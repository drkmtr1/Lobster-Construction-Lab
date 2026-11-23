# Pre-execution proof correction

The independent mathematical reviewer found an incorrect intermediate residual interval in the draft's B=8, a=3, u=12, T=11 row. The draft said the remaining weights were [1,6]. The complete complement is [1,8], and the unselected first terminal labeled 10 uses weight 7. The exact remainder is [1,6]∪{8}. The same remainder occurs at u=13 after subtracting weights 7 and 9.

The revised proof uses the remaining weight 8. It cannot arise at B=8 against zero or T=11 against low 3, since neither pinned low is incident to the necessary high on the original graph. The physical exit edge must use weight 8 and forces s:3=1. Its actual edge to T then gives forbidden weight 10. The correction was made before freezing the run inputs. It changes the justification for this case and preserves its conclusion.
