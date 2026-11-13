"""Container-only exact tests of Appendix D.2, paper v1.0.

The formal word route preserves multiplication order; the rational 2x2 route
differentiates actual matrix entries. Neither route solves the analytic ODE.
"""
import sympy as sp
import report


# An ordered word denotes a product in a free associative algebra. H=P^{-1};
# only adjacent PH or HP may cancel. No other pair of letters commutes.
def _word(xs):
    out=[]
    for x in xs:
        if out and (out[-1],x) in (('P','H'),('H','P')):
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def _clean(values):
    out={}
    for word,value in values.items():
        w=_word(word)
        out[w]=out.get(w,0)+value
    return {w:c for w,v in out.items() if (c:=sp.cancel(v))!=0}


def _add(*items):
    out={}
    for item in items:
        for w,c in item.items():out[w]=out.get(w,0)+c
    return _clean(out)


def _scale(c,item):return _clean({w:c*v for w,v in item.items()})
def _neg(item):return _scale(-1,item)
def _sub(left,right):return _add(left,_neg(right))


def _mul(*items):
    out={():sp.Integer(1)}
    for item in items:
        nxt={}
        for u,c in out.items():
            for v,d in item.items():
                w=_word(u+v)
                nxt[w]=nxt.get(w,0)+c*d
        out=_clean(nxt)
    return out


def _transpose(item):
    # P,Q,T and their inverse H are symmetric. Transposition reverses order.
    return _clean({tuple(reversed(w)):c for w,c in item.items()})


def _derivative(item,scalar_symbols):
    a,b,c,d=scalar_symbols
    letters={'P':{('Q',):sp.Integer(1)},
             'Q':{('T',):sp.Integer(1)},
             'T':{('U',):sp.Integer(1)},
             'H':{('H','Q','H'):sp.Integer(-1)}}
    out={}
    for w,value in item.items():
        scalar=sp.diff(value,a)*b+sp.diff(value,b)*c+sp.diff(value,c)*d
        out=_add(out,{w:scalar})
        for i,x in enumerate(w):
            if x not in letters:raise RuntimeError('Unexpected higher derivative')
            out=_add(out,_scale(value,_mul({w[:i]:sp.Integer(1)},letters[x],
                                         {w[i+1:]:sp.Integer(1)})))
    return _clean(out)


def _formal_checks():
    a,b,c,d=sp.symbols('a b c d',commutative=True)
    scalar_symbols=(a,b,c,d)
    I={():sp.Integer(1)}
    P={('P',):sp.Integer(1)}
    Q={('Q',):sp.Integer(1)}
    T={('T',):sp.Integer(1)}
    H={('H',):sp.Integer(1)}
    half=sp.Rational(1,2);threequarters=sp.Rational(3,4)
    du=lambda x:_derivative(x,scalar_symbols)
    dv=lambda x:_scale(1/a,du(x))
    # This derives the transformed derivatives using D_v=(1/f')D_u.
    Sv1=_scale(1/a,P)
    Sv2=dv(Sv1)
    Sv3=dv(Sv2)
    inverse_Sv1=_scale(a,H)
    A=_mul(H,Q)
    Av=_mul(inverse_Sv1,Sv2)
    assert _sub(_mul(H,Q),_mul(Q,H)), 'P inverse and Q must remain noncommuting'
    assert _sub(Av,_add(_scale(1/a,A),_scale(-b/a**2,I)))=={}
    Schu=_add(_scale(half,_mul(H,T)),_scale(-threequarters,_mul(A,A)))
    Schv=_add(_scale(half,_mul(inverse_Sv1,Sv3)),
              _scale(-threequarters,_mul(Av,Av)))
    scalar_schwarzian=c/a-sp.Rational(3,2)*(b/a)**2
    target=_scale(1/a**2,_add(Schu,_scale(-half*scalar_schwarzian,I)))
    assert _sub(Schv,target)=={}, 'Ordered matrix chain-rule residual'
    report.check('D2-MATRIX-CHAIN-RULE','Ordered matrix Schwarzian chain rule',True,
                 classification='symbolic-exact',
                 anchors=['eq:gg-intrinsic-matrix-schwarzian',
                          'eq:gg-intrinsic-projective-covariance'],
                 algebra='Free associative words with only adjacent P*H=H*P=1; exact rational scalar coefficients',
                 inputs='P=S_prime invertible; Q=S_double_prime; T=S_triple_prime; a=f_prime nonzero, b=f_double_prime, c=f_triple_prime',
                 result='S_v=f_prime^(-2)*(S_u-1/2*{f,u}*I)',
                 scope='Formal chain-rule identity with multiplication order retained; no ODE or global inverse theorem tested.')

    B=_scale(-half,_mul(Q,H))
    C=_neg(_add(_mul(B,B),du(B)))
    S={('S',):sp.Integer(1)}
    identities={
        'gram_ODE':_sub(_add(_mul(_transpose(B),H),_mul(H,B)),du(H)),
        'symmetric_YtYprime':_sub(_transpose(_mul(H,B)),_mul(H,B)),
        'Z_Jacobi':_add(_scale(2,_mul(B,P)),Q),
        'Wronskian':_sub(_mul(H,P),I),
        'Z_self_Wronskian':_add(
            _mul(S,_sub(_mul(H,B),_mul(_transpose(B),H)),S),
            _mul(S,H,P),_neg(_mul(P,H,S))),
        'R_symmetric':_sub(_transpose(_mul(H,C)),_mul(H,C)),
        'transpose_conjugacy':_sub(_transpose(C),Schu),
    }
    assert all(value=={} for value in identities.values()), identities
    report.check('D2-JACOBI-ALGEBRA','Normalization and Jacobi algebra, including transpose',True,
                 classification='symbolic-exact',
                 anchors=['eq:gg-intrinsic-jacobi-normalization',
                          'eq:gg-intrinsic-jacobi-identities',
                          'eq:gg-intrinsic-schwarzian-conjugacy'],
                 verified=list(identities),
                 definitions='Y_prime=Y*B, B=-Q*P_inverse/2, Z=Y*S, R=-Y_double_prime*Y_inverse; C=Y_inverse*R*Y',
                 conditions='S,P,Q,T symmetric; Y invertible and Y_transpose*Y=P_inverse',
                 scope='Conditional algebra and preservation identities; existence and ODE uniqueness used to obtain Y are not executed.')


def _cancel_matrix(value):return value.applyfunc(sp.cancel)


def _matrix_equal(left,right):
    return all(sp.cancel(x)==0 for x in left-right)


def _rational_matrix_checks():
    u=sp.symbols('u')
    # Rational symmetric graph. Its first and second derivative matrices do
    # not commute, even at the regular base point u=0.
    S=sp.Matrix([[1+u/(1-u),2+u**2/(2*(1+u))],
                 [2+u**2/(2*(1+u)),1+2*u+u**3/(3*(1-u))]])
    P=_cancel_matrix(S.diff(u));Q=_cancel_matrix(P.diff(u));T=_cancel_matrix(Q.diff(u))
    Pinv=_cancel_matrix(P.inv());A=_cancel_matrix(Pinv*Q)
    assert P.subs(u,0).det()==2
    commutator_at_zero=(P*Q-Q*P).subs(u,0)
    assert commutator_at_zero!=sp.zeros(2)
    A_derivative=_cancel_matrix(A.diff(u))
    assert (A*A_derivative-A_derivative*A).subs(u,0)!=sp.zeros(2)
    Schu=_cancel_matrix(sp.Rational(1,2)*Pinv*T-sp.Rational(3,4)*A*A)
    f=u+u**2;fp=sp.diff(f,u)
    dv=lambda matrix:_cancel_matrix(matrix.diff(u)/fp)
    Sv1=dv(S);Sv2=dv(Sv1);Sv3=dv(Sv2)
    Av=_cancel_matrix(Sv1.inv()*Sv2)
    Schv=_cancel_matrix(sp.Rational(1,2)*Sv1.inv()*Sv3-sp.Rational(3,4)*Av*Av)
    scalar_schwarzian=sp.diff(f,u,3)/fp-sp.Rational(3,2)*(sp.diff(f,u,2)/fp)**2
    expected=_cancel_matrix((Schu-sp.Rational(1,2)*scalar_schwarzian*sp.eye(2))/fp**2)
    assert _matrix_equal(Schv,expected)
    kappau=sp.trace(Schu)/2;kappav=sp.trace(Schv)/2
    assert sp.cancel(kappav-(kappau-scalar_schwarzian/2)/fp**2)==0
    # An algebraic initial factor and ODE-generated jets suffice to check the
    # displayed normalization, Wronskians and transpose at one actual point.
    Y0=sp.diag(1,1/sp.sqrt(2));P0=P.subs(u,0)
    B=-Q*Pinv/2;B0=B.subs(u,0);Bd0=B.diff(u).subs(u,0)
    Y1=Y0*B0;Y2=Y0*(B0*B0+Bd0)
    R0=_cancel_matrix(-Y2*Y0.inv())
    S0=S.subs(u,0);Q0=Q.subs(u,0)
    Z0=Y0*S0;Z1=Y1*S0+Y0*P0;Z2=Y2*S0+2*Y1*P0+Y0*Q0
    assert _matrix_equal(Y0.T*Y0,P0.inv())
    assert _matrix_equal(Y0.T*Y1-Y1.T*Y0,sp.zeros(2))
    assert _matrix_equal(Y2+R0*Y0,sp.zeros(2))
    assert _matrix_equal(Z2+R0*Z0,sp.zeros(2))
    assert _matrix_equal(Y0.T*Z1-Y1.T*Z0,sp.eye(2))
    assert _matrix_equal(Z0.T*Z1-Z1.T*Z0,sp.zeros(2))
    assert _matrix_equal(R0,R0.T)
    assert _matrix_equal(Schu.subs(u,0),(Y0.inv()*R0*Y0).T)
    report.check('D2-RATIONAL-MATRIX','Noncommuting rational symmetric graph and initial Jacobi jets',True,
                 classification='symbolic-exact',
                 anchors=['eq:gg-intrinsic-matrix-schwarzian',
                          'eq:gg-intrinsic-jacobi-normalization',
                          'eq:gg-intrinsic-jacobi-identities',
                          'eq:gg-intrinsic-schwarzian-conjugacy',
                          'eq:gg-intrinsic-projective-covariance'],
                 graph=str(S),coordinate_change=str(f),
                 determinant_Sprime_at_zero=str(P0.det()),
                 noncommuting_P_Q_at_zero=str(commutator_at_zero),
                 noncommuting_A_Aprime_at_zero=str((A*A_derivative-A_derivative*A).subs(u,0)),
                 R_at_zero=str(R0),kappa_at_zero=str(sp.cancel(kappau.subs(u,0))),
                 domain='A neighborhood of u=0 excluding poles u=+/-1 and zeros of det(S_prime) or f_prime=1+2u',
                 scope='Exact rational coordinate identity and algebraic initial jets; not an analytic ODE solve or a general graph-frame invariance test.')


def run(profile=None):
    _formal_checks()
    _rational_matrix_checks()
