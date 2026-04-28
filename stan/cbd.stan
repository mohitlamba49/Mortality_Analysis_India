
data {
  int N; int A; int Y;
  array[N] int D;
  vector[N] E;
  array[N] int age;
  array[N] int year;
}
parameters {
  vector[A] alpha;
  vector[Y] k1;
  vector[Y] k2;
}
model {
  k1 ~ normal(0,1);
  k2 ~ normal(0,0.5);

  for(n in 1:N)
    D[n] ~ poisson_log(
      log(E[n]) +
      alpha[age[n]] +
      k1[year[n]] +
      (age[n] - mean(age)) * k2[year[n]]
    );
}
generated quantities {
  vector[N] log_lik;
  for(n in 1:N)
    log_lik[n] = poisson_log_lpmf(
      D[n] |
      log(E[n]) +
      alpha[age[n]] +
      k1[year[n]] +
      (age[n] - mean(age)) * k2[year[n]]
    );
}
