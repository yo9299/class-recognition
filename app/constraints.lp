:- order(X,Y), order(Y,Z), not order(X,Z).
:- order(X,Y), order(Y,X).
  1 { order(X,Y); order(Y,X) } 1 :- vertex(X), vertex(Y), X != Y.
 :-order(X0, X1),edge(X0, X2),not edge(X0, X1).
 edge(X,Y) :- edge(Y,X).