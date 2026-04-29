% -------- GENDER FACTS -------- %
male(raj_kaul). male(vishwanath_nehru). male(mansaram_nehru). 
male(lakshminarayan_nehru). male(gangadhar_nehru). male(bansi_dhar_nehru). 
male(nandlal_nehru). male(motilal_nehru). male(brijlal_nehru). 
male(jawaharlal_nehru). male(ranjit_pandit). male(raja_hutheesing).
male(braj_kumar_nehru). male(feroze_gandhi). male(rajiv_gandhi). 
male(sanjay_gandhi). male(rahul_gandhi). male(varun_gandhi). 
male(robert_vadra). male(raihan_vadra).

female(jeorani_nehru). female(swarup_rani). female(kamala_nehru). 
female(vijaya_lakshmi_pandit). female(krishna_hutheesing). 
female(indira_gandhi). female(sonia_gandhi). female(maneka_gandhi). 
female(nayantara_sahgal). female(priyanka_gandhi). female(miraya_vadra). 
female(yamini_gandhi). female(anasuya_gandhi).

% -------- PARENT RELATIONSHIPS -------- %
% Ancestors
parent(raj_kaul, vishwanath_nehru).
parent(vishwanath_nehru, mansaram_nehru).
parent(mansaram_nehru, lakshminarayan_nehru).
parent(lakshminarayan_nehru, gangadhar_nehru).

% Motilal's Generation (Gangadhar's Sons)
parent(gangadhar_nehru, bansi_dhar_nehru).
parent(gangadhar_nehru, nandlal_nehru).
parent(gangadhar_nehru, motilal_nehru).
parent(jeorani_nehru, motilal_nehru).

% Jawaharlal's Siblings
parent(motilal_nehru, jawaharlal_nehru).
parent(swarup_rani, jawaharlal_nehru).
parent(motilal_nehru, vijaya_lakshmi_pandit).
parent(swarup_rani, vijaya_lakshmi_pandit).
parent(motilal_nehru, krishna_hutheesing).
parent(swarup_rani, krishna_hutheesing).

% Indira's Line
parent(jawaharlal_nehru, indira_gandhi).
parent(kamala_nehru, indira_gandhi).
parent(indira_gandhi, rajiv_gandhi).
parent(feroze_gandhi, rajiv_gandhi).
parent(indira_gandhi, sanjay_gandhi).
parent(feroze_gandhi, sanjay_gandhi).

% Rajiv & Sanjay's Descendants
parent(rajiv_gandhi, rahul_gandhi).
parent(sonia_gandhi, rahul_gandhi).
parent(rajiv_gandhi, priyanka_gandhi).
parent(sonia_gandhi, priyanka_gandhi).
parent(sanjay_gandhi, varun_gandhi).
parent(maneka_gandhi, varun_gandhi).

% Current Generation
parent(priyanka_gandhi, raihan_vadra).
parent(robert_vadra, raihan_vadra).
parent(priyanka_gandhi, miraya_vadra).
parent(robert_vadra, miraya_vadra).
parent(varun_gandhi, anasuya_gandhi).
parent(yamini_gandhi, anasuya_gandhi).

% Extended Cousins (Nandlal's branch)
parent(nandlal_nehru, brijlal_nehru).
parent(brijlal_nehru, braj_kumar_nehru).

% -------- RELATIONSHIP RULES -------- %
father(X,Y) :- parent(X,Y), male(X).
mother(X,Y) :- parent(X,Y), female(X).

child(X,Y) :- parent(Y,X).
son(X,Y) :- child(X,Y), male(X).
daughter(X,Y) :- child(X,Y), female(X).

sibling(X,Y) :- parent(P,X), parent(P,Y), X \= Y.
brother(X,Y) :- sibling(X,Y), male(X).
sister(X,Y) :- sibling(X,Y), female(X).

grandparent(X,Y) :- parent(X,Z), parent(Z,Y).
grandfather(X,Y) :- grandparent(X,Y), male(X).
grandmother(X,Y) :- grandparent(X,Y), female(X).

husband(X,Y) :- parent(X,C), parent(Y,C), male(X), female(Y).
wife(X,Y) :- husband(Y,X).

uncle(X,Y) :- brother(X,Z), parent(Z,Y).
aunt(X,Y) :- sister(X,Z), parent(Z,Y).

cousin(X,Y) :- parent(A,X), parent(B,Y), sibling(A,B), X \= Y.

ancestor(X,Y) :- parent(X,Y).
ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y).
