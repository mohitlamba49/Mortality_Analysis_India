// CBD-inspired log-rate benchmark (CBD-LR).
// This is the exact fitted specification used in the reported comparison.
// It is not the canonical older-age CBD model on the logit(q_x,t) scale.
data {
  int<lower=1> N; int<lower=1> A; int<lower=2> T;
  array[N] int<lower=1, upper=A> age;
  array[N] int<lower=1, upper=T> year;
  array[N] int<lower=0> deaths;
  vector<lower=0>[N] exposure; vector[A] age_value;
}
parameters {
  vector[A] alpha; vector[T - 1] z_k1; vector[T - 1] z_k2;
  real<lower=1e-4> sigma_k1; real<lower=1e-4> sigma_k2;
  real<lower=0.01> phi;
}
transformed parameters {
  vector[T] k1_unc; vector[T] k2_unc; vector[T] k1; vector[T] k2;
  k1_unc[1] = 0; k2_unc[1] = 0;
  for (t in 2:T) {
    k1_unc[t] = k1_unc[t - 1] + sigma_k1 * z_k1[t - 1];
    k2_unc[t] = k2_unc[t - 1] + sigma_k2 * z_k2[t - 1];
  }
  k1 = k1_unc - mean(k1_unc);
  k2 = k2_unc - mean(k2_unc);
}
model {
  vector[A] age_ctr = age_value - mean(age_value);
  alpha ~ normal(-5, 3); z_k1 ~ std_normal(); z_k2 ~ std_normal();
  sigma_k1 ~ exponential(1); sigma_k2 ~ exponential(1);
  phi ~ gamma(2, 0.1);
  for (n in 1:N)
    deaths[n] ~ neg_binomial_2_log(log(exposure[n]) + alpha[age[n]]
                                   + k1[year[n]]
                                   + age_ctr[age[n]] * k2[year[n]], phi);
}
generated quantities {
  vector[N] log_lik; vector[A] age_ctr = age_value - mean(age_value);
  for (n in 1:N)
    log_lik[n] = neg_binomial_2_log_lpmf(deaths[n] | log(exposure[n])
      + alpha[age[n]] + k1[year[n]]
      + age_ctr[age[n]] * k2[year[n]], phi);
}
