
data {
  int N; int A; int Y;
  array[N] int D;
  vector[N] E;
  array[N] int age;
  array[N] int year;
}
parameters {
  vector[A] alpha;
  simplex[A] beta;
  vector[Y] kappa_raw;
  real<lower=1e-6> sigma_kappa;
}
transformed parameters {
  vector[Y] kappa = kappa_raw - mean(kappa_raw);
}
model {
  alpha ~ normal(0,2);
  sigma_kappa ~ exponential(1);

  kappa_raw[1] ~ normal(0,1);
  for(t in 2:Y)
    kappa_raw[t] ~ normal(kappa_raw[t-1], sigma_kappa);

  for(n in 1:N)
    D[n] ~ poisson_log(log(E[n]) + alpha[age[n]] + beta[age[n]] * kappa[year[n]]);
}
generated quantities {
  vector[N] log_lik;
  for(n in 1:N)
    log_lik[n] = poisson_log_lpmf(D[n] | log(E[n]) + alpha[age[n]] + beta[age[n]] * kappa[year[n]]);
}
