data {
  int<lower=1> N; int<lower=1> A; int<lower=2> T; int<lower=3> C;
  int<lower=1> S;
  array[N] int<lower=1, upper=A> age;
  array[N] int<lower=1, upper=T> year;
  array[N] int<lower=1, upper=C> cohort;
  array[N] int<lower=1, upper=S> sex;
  array[N] int<lower=0> deaths;
  vector<lower=0>[N] exposure; vector[C] cohort_value;
}
parameters {
  matrix[A, S] alpha; array[S] simplex[A] beta;
  vector[T - 1] z_kappa; matrix[C - 1, S] z_gamma;
  real<lower=1e-4> sigma_kappa;
  vector<lower=1e-4>[S] sigma_gamma; vector<lower=0.01>[S] phi;
}
transformed parameters {
  vector[T] kappa_unc; vector[T] kappa;
  matrix[C, S] gamma_unc; matrix[C, S] gamma;
  vector[C] cohort_ctr = cohort_value - mean(cohort_value);
  real cohort_ss = dot_self(cohort_ctr);
  kappa_unc[1] = 0;
  for (t in 2:T)
    kappa_unc[t] = kappa_unc[t - 1] + sigma_kappa * z_kappa[t - 1];
  kappa = kappa_unc - mean(kappa_unc);
  for (s in 1:S) {
    vector[C] centered; real slope;
    gamma_unc[1, s] = 0;
    for (c in 2:C)
      gamma_unc[c, s] = gamma_unc[c - 1, s]
                        + sigma_gamma[s] * z_gamma[c - 1, s];
    centered = gamma_unc[, s] - mean(gamma_unc[, s]);
    slope = dot_product(cohort_ctr, centered) / cohort_ss;
    gamma[, s] = centered - slope * cohort_ctr;
  }
}
model {
  to_vector(alpha) ~ normal(-5, 3); z_kappa ~ std_normal();
  to_vector(z_gamma) ~ std_normal(); sigma_kappa ~ exponential(1);
  sigma_gamma ~ exponential(1); phi ~ gamma(2, 0.1);
  for (n in 1:N) {
    real eta = alpha[age[n], sex[n]]
             + beta[sex[n]][age[n]] * kappa[year[n]]
             + gamma[cohort[n], sex[n]];
    deaths[n] ~ neg_binomial_2_log(log(exposure[n]) + eta, phi[sex[n]]);
  }
}
generated quantities {
  vector[N] log_lik;
  for (n in 1:N) {
    real eta = alpha[age[n], sex[n]]
             + beta[sex[n]][age[n]] * kappa[year[n]]
             + gamma[cohort[n], sex[n]];
    log_lik[n] = neg_binomial_2_log_lpmf(deaths[n] |
      log(exposure[n]) + eta, phi[sex[n]]);
  }
}
