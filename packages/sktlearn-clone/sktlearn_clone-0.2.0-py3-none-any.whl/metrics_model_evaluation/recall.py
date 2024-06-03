from collections import defaultdict

def recall_score(y_true, y_pred, average='binary'):
    """
    Compute recall score of the model.
    
    Parameters:
        y_true : array-like of shape (n_samples,)
            True labels.
        y_pred : array-like of shape (n_samples,)
            Predicted labels.
        average : str, default='binary'
            Averaging strategy to apply. Possible values are {'micro', 'macro', 'binary', None}.
            If None, return recall for each class.
    
    Returns:
        recall : float or array of float
            Recall score(s).
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Lengths of y_true and y_pred must be the same.")
    
    if average == 'binary':
        # Calculate true positives and false negatives for binary classification
        tp = sum((true == 1) and (pred == 1) for true, pred in zip(y_true, y_pred))
        fn = sum((true == 1) and (pred == 0) for true, pred in zip(y_true, y_pred))
        
        # Calculate recall
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        
        return recall
    
    elif average in {'micro', 'macro', None}:
        # Calculate true positives and false negatives for multi-class classification
        tp = defaultdict(int)
        fn = defaultdict(int)
        
        for true, pred in zip(y_true, y_pred):
            if true == pred:
                tp[true] += 1
            else:
                fn[true] += 1
        
        if average == 'micro':
            # Calculate micro-averaged recall
            micro_tp = sum(tp.values())
            micro_fn = sum(fn.values())
            
            recall = micro_tp / (micro_tp + micro_fn) if micro_tp + micro_fn > 0 else 0
        else:  # average == 'macro' or average == None
            # Calculate recall for each class
            recall = {}
            for label in set(y_true + y_pred):
                tp_label = tp[label]
                fn_label = fn[label]
                recall[label] = tp_label / (tp_label + fn_label) if tp_label + fn_label > 0 else 0
            
            if average == 'macro':
                # Calculate macro-averaged recall
                recall = sum(recall.values()) / len(recall) if len(recall) > 0 else 0
            else:  # average == None
                # Return recall for each class
                return list(recall.values())
        
        return recall
    
    else:
        raise ValueError("Invalid value for 'average'.")
