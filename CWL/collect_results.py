import sys
acc = 0
auc = 0

br = 0
for i in range(1,len(sys.argv)):
    acc_cur, auc_cur = sys.argv[i].strip().split()
    print(f"Accuracy: {acc_cur}, AUC: {auc_cur}")
    
    acc_cur = float(acc_cur)
    auc_cur = float(auc_cur)
    
    acc += acc_cur
    auc += auc_cur
    br += 1

print(f"\n\nFinal accuracy: {acc/br}, Final AUC: {auc/br}")
    