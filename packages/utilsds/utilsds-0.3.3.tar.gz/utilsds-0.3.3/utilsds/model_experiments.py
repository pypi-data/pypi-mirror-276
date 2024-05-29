'''
Model function
'''
from datetime import datetime
from functools import partial
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score, recall_score, \
    fbeta_score, accuracy_score, confusion_matrix
from google.cloud import aiplatform
from hyperopt import fmin, tpe, STATUS_OK, Trials, space_eval

import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Lin Libertine']

#pylint: disable=attribute-defined-outside-init
#pylint: disable=raise-missing-from
#pylint: disable=invalid-name
#pylint: disable=dangerous-default-value
#pylint: disable=too-many-arguments
#pylint: disable=too-many-locals
#pylint: disable=too-many-instance-attributes

class Modeling:
    """Modeling and presentation of results"""

    def __init__(self,
                 model,
                 X_train: pd.DataFrame,
                 X_val: pd.DataFrame,
                 y_train: pd.Series,
                 y_val: pd.Series,
                 name_experiment: str,
                 data_path: str,
                 labels=["0","1"],
                 beta=2):
        """
        Parameters
        ----------
        model : model name
            Name of model without round brackets
        X_train : d.DataFrame
            Data with all columns to train model (with id_client)
        X_val : pd.DataFrame
            Data with all columns to validate model (with id_client)
        y_train : pd.Series
            Target variable to train data
        y_val : pd.Series
            Target variable to validate data
        name_experiment : str
            Name of main experinemts where run will be safed.
        data_path : str
            Path to data from GCS.
        labels : array-like, optional
            The set of labels to include when average != 'binary', and their order if 
            average is None. Labels present in the data can be excluded, for example 
            to calculate a multiclass average ignoring a majority negative class, while 
            labels not present in the data will result in 0 components in a macro average.
            For multilabel targets, labels are column indices. By default, all labels 
            in y_true and y_pred are used in sorted order, by default ["0","1"]
        beta : int, optional
            Value of beta for fbeta_score. Determines the weight of recall in the combined score,
            by default 2
        average_for_f1 : str, optional
            his parameter is required for multiclass/multilabel targets. If None, the scores 
            for each class are returned. 
            Possible choice: {'micro', 'macro', 'samples', 'weighted', binary', None},
            by default None
        """

        self.model = model
        if 'id_client' in X_train.columns:
            self.X_train = X_train.drop('id_client', axis=1)
        else:
            self.X_train = X_train
        self.y_train = y_train
        if 'id_client' in X_val.columns:
            self.X_test = X_val.drop('id_client', axis=1)
        else:
            self.X_test = X_val
        self.y_test = y_val
        self.labels = labels
        self.beta = beta
        self.name_experiment = name_experiment
        self.data_path = data_path
        self.project='sts-notebooks'
        self.location='europe-west4'
        self.proba = 0.5
        self.random_state=2024

    def calculate_f_beta_score(self, y_test, y_pred):
        """
        Calculate fbeta score

        Parameters
        ----------
        y_test : pd.Series
            Target variable of test data
        y_pred : pd.Series
            Target variable of prediction model

        Returns
        -------
        float
            fbeta_score
        """

        score = fbeta_score(y_test, y_pred, beta=self.beta)
        return round(score, 4)

    def classifier_selection(self, params):
        """
        Model selection

        Parameters
        ----------
        params : dict
            Dict of hyperparameter for model

        Returns
        -------
        model
            Return model instance.
        """

        if params:
            return self.model(**params)
        return self.model(random_state=self.random_state)

    def fit_predict(self, params=None):
        """
        Function to train, predict our model
        
        Parameters
        ----------
        params : dict
            Dict of hyperparameter for model
        """

        classifier = self.classifier_selection(params)

        classifier.fit(self.X_train.values, self.y_train.values.ravel())
        self.y_pred = classifier.predict(self.X_test.values)

        self.classifier = classifier

        self.experiment_results(self.y_test, self.y_pred)

        print(f'''--------------------------------------------- \
        F beta score: {self.calculate_f_beta_score(self.y_test, self.y_pred)} \
        -------------------------------------------\n''')

    def fit_predict_proba(self, params=None, proba=0.5):
        """
        Function to train, predict our model
        
        Parameters
        ----------
        params : dict
            Dict of hyperparameter for model
        """
        self.proba = proba
        classifier = self.classifier_selection(params)

        classifier.fit(self.X_train.values, self.y_train.values.ravel())
        self.y_pred = (classifier.predict_proba(self.X_test.values)[:,1] >= proba).astype(bool)

        self.classifier = classifier

        self.experiment_results(self.y_test, self.y_pred)

        print(f'''--------------------------------------------- \
        F beta score: {self.calculate_f_beta_score(self.y_test, self.y_pred)} \
        -------------------------------------------\n''')


    def stratified_cross_val(self, params=None, n_splits=5):
        """
        Calculate average f beta score from StratifiedKfold

        Parameters
        ----------
        params : dict
            Dict of hyperparameter for model
        n_splits: int, default=5
            Number of folds. Must be at least 2.
        """

        model_stratified = self.classifier_selection(params)
        X = np.array(pd.concat([self.X_train, self.X_test]
                         ,ignore_index=True))
        y = np.array(pd.concat([self.y_train, self.y_test]
                         ,ignore_index=True))
        scores = []
        for train_idx, test_idx in StratifiedKFold(n_splits=n_splits,
                                                   random_state=self.random_state,
                                                   shuffle=True).split(X, y):
            model_stratified.fit(X[train_idx], y[train_idx].ravel())
            y_pred_stratified = model_stratified.predict(X[test_idx])

            scores.append(self.calculate_f_beta_score(y[test_idx], y_pred_stratified))

        print(f'''-------------------------- For stratified fold: Mean F beta score = \
        {np.mean(scores)}; std = {np.std(scores)} -------------------------\n''')


    def objective(self, params):
        """
        Function for hyperopt to fit predict and calculate loss
        
        Parameters
        ----------
        params : dict
            Dict of hyperparameter for model
        """

        model = self.model(**params)
        model.fit(self.X_train, self.y_train.values.ravel())
        y_pred = model.predict(self.X_test)

        return{'loss':-1*self.calculate_f_beta_score(self.y_test, y_pred), 'status': STATUS_OK }

    def hyperopt_best_params(self, space, n_startup_jobs=5, hyperopt_iter=100):
        """
        Calculate models and return the best parameters in variable self.best_params.

        Parameters
        ----------
        space : dict
            Dict of parameter space, example: "'C': hp.uniform('C', 0.1, 100)"
        n_startup_jobs : int, optional
            Number of random hyperparameters search, by default 5
        hyperopt_iter : int, optional
            Number of iteration for hyperopt, by default 100
        """

        self.trials = Trials()
        self.best_params = fmin(fn=self.objective,
                    space=space,
                    algo=partial(tpe.suggest, n_startup_jobs=n_startup_jobs),
                    max_evals=hyperopt_iter,
                    trials=self.trials)

        self.best_params = space_eval(space, self.best_params)

        print(f"The best params: {self.best_params}\n")

    def classification_metrics(self, y_true: pd.Series, y_pred: pd.Series):
        """ Calculate and write confusion matrix in vertex experiment.

        Parameters
        ----------
        y_true : pd.Series
            Values of true target variable 
        y_pred : pd.Series
            Values of predicted target variable 
        """
        aiplatform.log_classification_metrics(
                labels=self.labels,
                matrix=confusion_matrix(y_true, y_pred,).tolist(),
                display_name="confusion-matrix",
            )

    def calculate_metrics(self, y_true: pd.Series, y_pred: pd.Series):
        """ Calculate all metrics.

        Parameters
        ----------
        y_true : pd.Series
            Values of true target variable 
        y_pred : pd.Series
            Values of predicted target variable

        Returns
        -------
        metrics
            Dictionary of all calculated metrics.
        """
        tn, fp, fn, tp = confusion_matrix(self.y_test, y_pred).ravel()
        specificity = tn / (tn+fp)
        metrics = {}
        metrics['specificity'] = specificity
        metrics['fbeta_score'] = self.calculate_f_beta_score(self.y_test, self.y_pred)
        metrics['accuracy_score'] = accuracy_score(y_true, y_pred)
        metrics['precision_score'] = precision_score(y_true, y_pred)
        metrics['recall_score'] = recall_score(y_true, y_pred)
        return metrics

    def hyperparams_model(self):
        """ Return all hyperparameters of model, data path and all data columns.

        Returns
        -------
        params
            All params.
        """
        params = {key: value for key, value in
                  self.classifier.get_params().items() if value is not None and value is not np.nan}
        params['data_path'] = self.data_path
        params['proba'] = self.proba
        params['feature_names'] = str(self.X_train.columns.tolist())
        return params

    def experiment_results(self, y_true: pd.Series, y_pred: pd.Series):
        """ The function saves all values (params, metrics) on Vertex experiments.

        Parameters
        ----------
        y_true : pd.Series
            Values of true target variable 
        y_pred : pd.Series
            Values of predicted target variable

        Raises
        ------
        TypeError
        """
        aiplatform.init(
            project=self.project,
            location=self.location,
            experiment=self.name_experiment,
            experiment_tensorboard=False,
            )

        run_name = f'''{type(self.classifier).__name__.lower()
                        }{datetime.now().strftime("%Y%m%d%H%M%S")}'''
        aiplatform.start_run(run_name)

        params = self.model().get_params()
        params['data_path'] = self.data_path

        try:
            aiplatform.log_params(self.hyperparams_model())
            aiplatform.log_metrics(self.calculate_metrics(y_true, y_pred))
            self.classification_metrics(y_true, y_pred)
            aiplatform.end_run()

        except TypeError:
            aiplatform.end_run()
            experiment_run = aiplatform.ExperimentRun(
                run_name=run_name,
                experiment=self.name_experiment,
                project=self.project,
                location=self.location
                )
            experiment_run.delete()
            raise TypeError(f'TypeError: Change parameters. Experiment_run {run_name} was removed.')


    def plot_confusion_matrix(self, y_pred):
        """
        Plot confusion matrix for model results
        
        Parameters
        ----------
        y_pred : pd.Series
            Target variable of prediction model
        """

        plt.figure(figsize=(4, 3), facecolor='w')
        sns.heatmap(confusion_matrix(self.y_test, y_pred), annot=True, fmt='.0f', cbar=False,
                    vmax=confusion_matrix(self.y_test, y_pred).max(), vmin=0, cmap='Blues')
        plt.xlabel('Predicted label')
        plt.ylabel('True label')
        plt.title(f'Confusion matrix for {type(self.model()).__name__}')

    def plot_confusion_matrix_percent(self, y_pred):
        """
        Plot confusion matrix with part of 1 value
        
        Parameters
        ----------
        y_pred : pd.Series
            Target variable of prediction model
        """

        plt.figure(figsize=(4, 3), facecolor='w')
        cm = confusion_matrix(self.y_test, y_pred)
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        df_cm = pd.DataFrame(cm_norm)
        sns.heatmap(df_cm, annot=True, cmap="Blues", cbar=False)
        plt.xlabel('Predicted label')
        plt.ylabel('True label')
        plt.title(f'Confusion matrix for {type(self.model()).__name__}')

    def plot_confusion_matrix_stats(self, y_pred):
        """
        Plot confusion matrix with percentage value of total.
        
        Parameters
        ----------
        y_pred : pd.Series
            Target variable of prediction model
        """
        cm = confusion_matrix(self.y_test, y_pred)

        TN = cm[0][0]
        TP = cm[1][1]
        print(f"Poprawność predykcji: {round((TN + TP) / len(y_pred) * 100, 2)}%")

        group_names = ['True Neg','False Pos','False Neg','True Pos']
        group_counts = [f"{value}" for value in cm.flatten()]
        group_percentages = [f"{round(value*100, 2)}%" for value in cm.flatten()/np.sum(cm)]
        labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(
            group_names,group_counts,group_percentages)]
        labels = np.asarray(labels).reshape(2,2)

        plt.figure(figsize=(4, 3), facecolor='w')
        sns.heatmap(cm, annot=labels, fmt='', cbar=False, vmin=0, cmap='Blues')
        plt.xlabel('Predicted label')
        plt.ylabel('True label')
        plt.title(f'Confusion matrix for {type(self.model()).__name__}')