
data {
  int N; int A; int Y; int C;
  array[N] int D;
  vector[N] E;
  array[N] int age;
  array[N] int year;
  array[N] int cohort;
}
parameters {
  vector[A] alpha;
  vector[Y] kappa_raw;
  vector[C] gamma_raw;
  real<lower=1e-6> sigma_kappa;
  real<lower=1e-6> sigma_gamma;
}
transformed parameters {
  vector[Y] kappa = kappa_raw - mean(kappa_raw);
  vector[C] gamma = gamma_raw - mean(gamma_raw);
}
model {
  alpha ~ normal(0,2);
  sigma_kappa ~ exponential(1);
  sigma_gamma ~ exponential(1);

  kappa_raw ~ normal(0, sigma_kappa);
  gamma_raw ~ normal(0, sigma_gamma);

  for(n in 1:N)
    D[n] ~ poisson_log(log(E[n]) + alpha[age[n]] + kappa[year[n]] + gamma[cohort[n]]);
}
generated quantities {
  vector[N] log_lik;
  for(n in 1:N)
    log_lik[n] = poisson_log_lpmf(D[n] | log(E[n]) + alpha[age[n]] + kappa[year[n]] + gamma[cohort[n]]);
}
