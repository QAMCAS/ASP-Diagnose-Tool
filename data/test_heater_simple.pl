% Simple temperature model comprising an external temperature input and a system 
% with an internal temperature. To be used as example for heating simulation.
% (C) 2021, F. Wotawa, TU Graz, Institute for Software Technology

% Pre-definition of the temperature range

next(between(t_max,t_up),t_max).
next(t_up,between(t_max,t_up)).
next(between(t_up,t_low), t_up).
next(t_low,between(t_up,t_low)).
next(between(t_low,null),t_low).
next(null, between(t_low,null)).

greater(X,Y) :- next(Y,X).
greater(X,Y) :- next(Z,X), greater(Z,Y).

smaller(X,Y) :- next(X,Y).
smaller(X,Y) :- next(X,Z), smaller(Z,Y).

inc(X,Y) :- next(X,Y), X != t_max.
inc(t_max,t_max).

dec(X,Y) :- next(Y,X), X != null.
dec(null, null).

% Determining the value of temperature using the predicate val(port, value, time)

val(int(S), Z, T+1) :- type(S, temp), val(int(S), W, T), greater(V,W), inc(W,Z).
val(int(S), Z, T+1) :- type(S, temp), val(int(S), W, T), smaller(V,W), dec(W,Z).

%%% Diagnosis model
type(tm, temp).
type(sw, switch).

comp(X) :- type(X,_).

nab(X) :- comp(X), not ab(X).
ab(X) :- comp(X), not nab(X).

no_ab(N) :- N = #count { C : ab(C) }.

:- not no_ab(1). % Search for single faults only

%time(T+1) :- time(T), T < 2.

% Controller behavior

on(sw,T+1) :- val(int(tm),V,T), smaller(V,t_up).
off(sw,T+1) :- val(int(tm),V,T), greater(V,t_up).
off(sw,T+1) :- val(int(tm),t_up,T).
:- on(sw,T), off(sw,T).


% Observations
on(sw,1).
off(sw,1).

%val(int(tm),null,0). % At the beginning there is no heat stored
%val(int(tm),null,1).
%val(int(tm),between(t_low,null),2). 
%val(int(tm),t_low,3). 
%val(int(tm),between(t_up,t_low),4). 
% val(int(tm),t_up,5).
% val(int(tm),between(t_max,t_up),6).
% val(int(tm),t_up,7). 
% val(int(tm),between(t_up,t_low),8).
% val(int(tm),t_low,9).
% val(int(tm),between(t_up,t_low),10). 
% val(int(tm),t_up,11). 
% val(int(tm),between(t_max,t_up),12). 
% val(int(tm),t_up,13).
% val(int(tm),between(t_up,t_low),14).
% val(int(tm),t_low,15).
% val(int(tm),between(t_up,t_low),16).

% Display values of temperature only

#show val/3.
#show on/2.
#show ab/1.
