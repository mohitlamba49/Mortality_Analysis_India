data {
  int<lower=1> N; int<lower=1> A; int<lower=2> T; int<lower=3> C;
  array[N] int<lower=1, upper=A> age;
  array[N] int<lower=1, upper=T> year;
  array[N] int<lower=1, upper=C> cohort;
  array[N] int<lower=0> deaths;
  vector<lower=0>[N] exposure; vector[C] cohort_value;
}
parameters {
  vector[A] alpha; vector[T - 1] z_kappa; vector[C - 1] z_gamma;
  real<lower=1e-4> sigma_kappa; real<lower=1e-4> sigma_gamma;
  real<lower=0.01> phi;
}
transformed parameters {
  vector[T] kappa_unc; vector[T] kappa;
  vector[C] gamma_unc; vector[C] gamma; vector[C] centered;
  vector[C] cohort_ctr = cohort_value - mean(cohort_value);
  real slope;
  kappa_unc[1] = 0;
  for (t in 2:T)
    kappa_unc[t] = kappa_unc[t - 1] + sigma_kappa * z_kappa[t - 1];
  kappa = kappa_unc - mean(kappa_unc);
  gamma_unc[1] = 0;
  for (c in 2:C)
    gamma_unc[c] = gamma_unc[c - 1] + sigma_gamma * z_gamma[c - 1];
  centered = gamma_unc - mean(gamma_unc);
  slope = dot_product(cohort_ctr, centered) / dot_self(cohort_ctr);
  gamma = centered - slope * cohort_ctr;
}
model {
  alpha ~ normal(-5, 3); z_kappa ~ std_normal(); z_gamma ~ std_normal();
  sigma_kappa ~ exponential(1); sigma_gamma ~ exponential(1);
  phi ~ gamma(2, 0.1);
  for (n in 1:N)
    deaths[n] ~ neg_binomial_2_log(log(exposure[n]) + alpha[age[n]]
                                   + kappa[year[n]] + gamma[cohort[n]], phi);
}
generated quantities {
  vector[N] log_lik;
  for (n in 1:N)
    log_lik[n] = neg_binomial_2_log_lpmf(deaths[n] | log(exposure[n])
      + alpha[age[n]] + kappa[year[n]] + gamma[cohort[n]], phi);
}
