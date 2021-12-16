import socium
import human
import random


random.seed(1)

X, Y = human.X_CHROMOSOME, human.Y_CHROMOSOME
M, N = human.MAG_CHROMOSOME, human.NMAG_CHROMOSOME


def TestSocium(iterations, starting_population, years_to_live):
    total, super_mages, mages = 0, 0, 0
    total_magi_born = 0
    for iteration in range(iterations):
        city = socium.ASocium()

        for i in range(starting_population):
            if i % 2 == 0:
                person = human.AHuman((X, Y), (N, N))
            else:
                person = human.AHuman((X, X), (N, N))
            city.AddHuman(person)
        for year in range(years_to_live+1):
            city.LiveOneYear()
            if year % 10 == 0:
                print(f"{year:4d}th year is passed. Current total magi born: {human.AHuman.GetTotalMagiBorn()}")
            # if year == year_of_mutation:
            #     woman = human.AHuman()
            #     city.AddHuman(woman)

        total += city.GetTotalPopulation()
        total_magi_born += human.AHuman.GetTotalMagiBorn()
        super_mages += city.GetCustomMageStatusPopulation(human.SUPER_MAGE)
        mages += city.GetCustomMageStatusPopulation(human.MAGE)
        print(f"Iter # {iteration} is done.")

    total = float(total) / iterations
    super_mages = float(super_mages) / iterations
    mages = float(mages) / iterations
    total_magi_born /= iterations
    print()
    print("Average total population         : {0:.3f}".format(total))
    print()
    print("Average mage population          : {0:.3f} ({1:2.2f}%)".format(mages, mages / total * 100))
    print("Average Super-mage population    : {0:.3f} ({1:2.2f}%)".format(super_mages, super_mages / total * 100))
    print(f"Average total magi born          : {total_magi_born}")


if __name__ == "__main__":
    import time
    t1 = time.time_ns()
    TestSocium(iterations=1, starting_population=100, years_to_live=1500)
    t2 = time.time_ns()
    print(f"Elapsed time: {(t2 - t1) / 1000000:.2f} ms")
