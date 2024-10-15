%Theorem 2.9 (Scott and Suppes [SS58]) A partial order relation S defined on V is a semiorder
%if the following conditions hold:
%1. S is irreflexive.
%2. (x, y) ∈ S and (z, w) ∈ S imply (x, w) ∈ S or (z, y) ∈ S.
%3. (x, y) ∈ S and (y, z) ∈ S imply (x, w) ∈ S or (w, z) ∈ S.
:- semiorder(X,Y), semiorder(Y,Z), not semiorder(X,Z).
:- semiorder(X,Y), semiorder(Y,X).
:- semiorder(X,Y), semiorder(Z,W), not semiorder(X,W), not semiorder(Z,Y).
:- semiorder(X,Y), semiorder(Y,Z), element(W), not semiorder(X,W), not semiorder(W,Z).

% Theorem 2.8 (Roberts [Rob69])
% There is a semiorder on S(V, P ) on the vertices of V such that (u, w) ∈ P ⇔ (u, w) 6∈ E(G).
% iff G is a unit interval graph.
{ semiorder(X,Y) } :- element(X), element(Y), X != Y.
:- element(X), element(Y), X!=Y, semiorder(X,Y), theedge(X,Y).
:- element(X), element(Y), X != Y, not semiorder(X,Y), not semiorder(Y,X), not theedge(X,Y).
%{debug}.

element(x(V)) :- vertex(V).
element(y(V)) :- vertex(V).
%1 { theedge(x(U), x(V)); theedge(x(U), y(V)); theedge(y(U), x(V)); theedge(y(U), y(V))} :- edge(U,V), U < V.
%1 { theedge(x(U), x(V)); theedge(x(U), y(V)); theedge(y(U), x(V)); theedge(y(U), y(V))} :- edge(V,U), U < V.
1 { theedge(x(U), x(V)); theedge(y(U), y(V))} :- edge(U,V), U < V.
1 { theedge(x(U), x(V)); theedge(y(U), y(V))} :- edge(V,U), U < V.
semiorder(x(V), y(V)) :- vertex(V).

%element(1..3).
%theedge(1,V) :- element(V), V > 1.
theedge(V,U) :- theedge(U,V).


%#show.
%#show theedge/2.
%#show element/1.
%#show semiorder/2.
%#show theedge(U,V) : theedge(U,V), U<V.
