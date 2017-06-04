using System;
using System.Linq;

namespace VS
{
    struct PDef
    {
        public long Color;
        public long Amount;
    }

    class Program
    {
        static void Main(string[] args)
        {
            long[] l = Console.ReadLine().Split(' ').Select(x => long.Parse(x)).ToArray();

            long d = l[0];
            long k = l[1];

            PDef[] p = new PDef[d];

            for (long i = 0; i < d; i++)
            {
                l = Console.ReadLine().Split(' ').Select(x => long.Parse(x)).ToArray();
                p[i] = new PDef()
                {
                    Color = l[0],
                    Amount = l[1],
                };
            }

            long result = Solve(p, k);

            Console.WriteLine(result);
        }

        static long Solve(PDef[] p, long k)
        {
            long n = p.Length;
            //# allocate array of (n + 1) rows and k + 1 columns
            //# D[n][k] to be a solution of original problem
            long[,] D = new long[n + 1, k + 1];

            long[,] d = PrecalculatePartialSums(p);

            //# iterate trough row in columns (columns iterated in outer loop)
            for (long m = 0; m <= k; m++)
            {
                for (long i = 0; i <= n; i++)
                {
                    if (i == 0 || m == 0 || m >= i)
                    {
                        D[i, m] = 0;
                        continue;
                    }

                    if (m == 1)
                    {
                        D[i, m] = d[0, i - 1];
                        continue;
                    }

                    long? DOptimal = null;

                    for (long j = m; j <= i; j++)
                    {
                        long DCurrent = D[j - 1, m - 1] + d[j - 1, i - 1];

                        if (DOptimal == null || DCurrent < DOptimal.Value)
                            DOptimal = DCurrent;
                    }

                    D[i, m] = DOptimal.Value;
                }
            }

            return D[n, k];
        }

        static T[] Slice<T>(T[] array, long i, long j)
        {
            T[] slice = new T[j - i + 1];

            Array.Copy(array, i, slice, 0, j - i + 1);

            return slice;
        }

        static long[,] PrecalculatePartialSums(PDef[] p)
        {
            long n = p.Length;
            long[,] precalculated = new long[n, n];

            for (long i = 0; i < n; i++)
            {
                for (long j = i; j < n; j++)
                {
                    PDef[] part = Slice(p, i, j);

                    long mean = WeightedMean(part);
                    precalculated[i, j] = SumOfSquaredDiffsTo(part, mean);
                }
            }

            return precalculated;
        }

        static long WeightedMean(PDef[] p)
        {
            long totalAmount = 0;
            long totalWeightedSum = 0;

            foreach (PDef pi in p)
            {
                totalAmount += pi.Amount;
                totalWeightedSum += pi.Color * pi.Amount;
            }

            return (long)Math.Round((totalWeightedSum / (double)totalAmount), 0);
        }

        static long SumOfSquaredDiffsTo(PDef[] p, long target)
        {
            long result = 0;

            foreach (PDef pi in p)
            {
                result += pi.Amount * (pi.Color - target) * (pi.Color - target);
            }

            return result;
        }
    }
}
