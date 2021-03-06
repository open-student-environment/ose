from pymc import Uniform, MCMC
from pylab import hist, show
from ose.statement import load_statements, load_file

from ose.environment import Environment
from ose.student import PoissonStudent


def main():
    s1 = PoissonStudent("arnaud", 1)
    s2 = PoissonStudent("francois", 1)
    s3 = PoissonStudent("david", 0.5)

    students = [s1, s2, s3]
    env = Environment(students)
    statements = env.simulate(1000, verbose=True)

    student_names = set(s['actor'] for s in statements)
    lam = Uniform('lam', lower=0, upper=1)
    students = [PoissonStudent(name=name, lam=lam) for name in student_names]
    env = Environment(students, statements)
    params = [lam]
    for s in students:
        params.extend(s.params)
    m = MCMC(params)
    m.sample(iter=10000, burn=1000, thin=10)
    hist(m.trace('lambda_david')[:])
    show()


def main2():
    data = load_file("statements-brneac3-20180301-20180531.json")
    statements = load_statements(data)
    user_name = "2890ebd9-1147-4f16-8a65-b7239bd54bd0"
    user_name = "2890ebd9-1147-4f16-8a65-b7239bd54bd0"
    lam = Uniform('lam', lower=0, upper=1)
    s1 = PoissonStudent(user_name, lam=lam)

    ## Creating environment and fitting data
    env = Environment([s1], statements)
    env.add_student(s1)
    res = env.fit([lam], method='mcmc')
    print(res)
    ## plotting. can be integrated in env
    hist(res.trace('lambda_{}'.format(user_name))[:])
    show()


if __name__ == '__main__':
    main2()
