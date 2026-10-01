data {
  int<lower=1> N; int<lower=1> A; int<lower=2> T;
  array[N] int<lower=1, upper=A> age;
  array[N] int<lower=1, upper=T> year;
  array[N] int<lower=0> deaths;
  vector<lower=0>[N] exposure;
}
parameters {
  vector[A] alpha; simplex[A] beta; vector[T - 1] z_kappa;
  real<lower=1e-4> sigma_kappa; real<lower=0.01> phi;
}
transformed parameters {
  vector[T] kappa_unc; vector[T] kappa;
  kappa_unc[1] = 0;
  for (t in 2:T)
    kappa_unc[t] = kappa_unc[t - 1] + sigma_kappa * z_kappa[t - 1];
  kappa = kappa_unc - mean(kappa_unc);
}
model {
  alpha ~ normal(-5, 3); z_kappa ~ std_normal();
  sigma_kappa ~ exponential(1); phi ~ gamma(2, 0.1);
  for (n in 1:N)
    deaths[n] ~ neg_binomial_2_log(log(exposure[n]) + alpha[age[n]]
                                   + beta[age[n]] * kappa[year[n]], phi);
}
generated quantities {
  vector[N] log_lik;
  for (n in 1:N)
    log_lik[n] = neg_binomial_2_log_lpmf(deaths[n] | log(exposure[n])
      + alpha[age[n]] + beta[age[n]] * kappa[year[n]], phi);
}
