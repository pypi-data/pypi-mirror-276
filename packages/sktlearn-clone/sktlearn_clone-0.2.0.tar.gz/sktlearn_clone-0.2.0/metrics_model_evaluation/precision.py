from collections import defaultdict

def precision_score(y_true, y_pred, average='binary'):
    """
    Compute precision score of the model.
    
    Parameters:
        y_true : array-like of shape (n_samples,)
            True labels.
        y_pred : array-like of shape (n_samples,)
            Predicted labels.
        average : str, default='binary'
            Averaging strategy to apply. Possible values are {'micro', 'macro', 'binary', None}.
            If None, return precision for each class.
    
    Returns:
        precision : float or array of float
            Precision score(s).
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Lengths of y_true and y_pred must be the same.")
    
    if average == 'binary':
        # Calculate true positives and false positives for binary classification
        tp = sum((true == 1) and (pred == 1) for true, pred in zip(y_true, y_pred))
        fp = sum((true == 0) and (pred == 1) for true, pred in zip(y_true, y_pred))
        
        # Calculate precision
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        
        return precision
    
    elif average in {'micro', 'macro', None}:
        # Calculate true positives and false positives for multi-class classification
        tp = defaultdict(int)
        fp = defaultdict(int)
        
        for true, pred in zip(y_true, y_pred):
            if true == pred:
                tp[true] += 1
            else:
                fp[pred] += 1
        
        if average == 'micro':
            # Calculate micro-averaged precision
            micro_tp = sum(tp.values())
            micro_fp = sum(fp.values())
            
            precision = micro_tp / (micro_tp + micro_fp) if micro_tp + micro_fp > 0 else 0
        else:  # average == 'macro' or average == None
            # Calculate precision for each class
            precision = {}
            for label in set(y_true + y_pred):
                tp_label = tp[label]
                fp_label = fp[label]
                precision[label] = tp_label / (tp_label + fp_label) if tp_label + fp_label > 0 else 0
            
            if average == 'macro':
                # Calculate macro-averaged precision
                precision = sum(precision.values()) / len(precision) if len(precision) > 0 else 0
            else:  # average == None
                # Return precision for each class
                return list(precision.values())
        
        return precision
    
    else:
        raise ValueError("Invalid value for 'average'.")
