def solutions_strong_fault():
    # Search only for solutions with strong fault models
    constraint = "%s0(X) :- comp(X), not ns0(X). \
        %ns0(X) :- comp(X), not s0(X). \
        %s1(X) :- comp(X), not ns1(X). \
        %ns1(X) :- comp(X), not s1(X). \
        ab(X) :- s0(X). % All stuck-at faults are also faults \
        ab(X) :- s1(X). \
        :- s0(X), s1(X). % Only one stuck-at fault is possible at a time. \
        out(X,0) :- s0(X). % Behavior of stuck-at faults \
        out(X,1) :- s1(X). \
        :- 0 = #count { C : s0(C); D : s1(D) }."
    return constraint

def solutions_without_strong_fault():
    # Search only for solutions without strong fault models
    constraint = "%s0(X) :- comp(X), not ns0(X). \
        %ns0(X) :- comp(X), not s0(X). \
        %s1(X) :- comp(X), not ns1(X). \
        %ns1(X) :- comp(X), not s1(X). \
        ab(X) :- s0(X). % All stuck-at faults are also faults \
        ab(X) :- s1(X). \
        :- s0(X), s1(X). % Only one stuck-at fault is possible at a time. \
        out(X,0) :- s0(X). % Behavior of stuck-at faults \
        out(X,1) :- s1(X). \
        :- 0 < #count { C : s0(C); D : s1(D) }."
    return constraint