%linear order constraints
:- order(X,Y), order(Y,Z), not order(X,Z).
:- order(X,Y), order(Y,X).
%:- not order(X,Y), not order(Y,X).

%every pair of vertices can belong to the order
1 { order(X,Y); order(Y,X) } 1 :- vertex(X), vertex(Y), X != Y.

%element(X) :- vertex(V).
:- order(X,Y), order(Y,Z), edge(X,Z), not edge(X, Y). 

edge(X,Y) :- edge(Y,X).