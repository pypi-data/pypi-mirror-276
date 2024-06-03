def make_scorer(score_func):
    # TODO: to be modified (necessarly)
    """Make a scorer from a performance metric or loss function.

    Parameters:
    score_func : callable
        Score function (or loss function) with signature score_func(y_true, y_pred).

    Returns:
    callable
        Scorer object that wraps the provided score function.
    """
    def scorer(estimator, X, y_true):
        """Scoring function that wraps the provided score_func."""
        y_pred = estimator.predict(X)
        return score_func(y_true, y_pred)

    return scorer
