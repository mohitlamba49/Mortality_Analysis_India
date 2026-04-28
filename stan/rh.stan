
data {
  int<lower=1> N;
  int<lower=1> A;
  int<lower=1> T;
  int<lower=1> C;
  int<lower=1> S;

  array[N] int age;
  array[N] int year;
  array[N] int cohort;
  array[N] int sex;
  array[N] int deaths;
  vector[N] exposure;
}

parameters {
  matrix[A, S] alpha;
  matrix[A, S] beta;
  vector[T] kappa_raw;
  matrix[C, S] gamma_raw;

  real<lower=0> sigma_kappa;
  real<lower=0> sigma_gamma;
  real<lower=0> phi;
}

transformed parameters {
  vector[T] kappa = kappa_raw - mean(kappa_raw);
  matrix[C, S] gamma;

  for (s in 1:S)
    gamma[, s] = gamma_raw[, s] - mean(gamma_raw[, s]);
}

model {
  to_vector(alpha) ~ normal(0, 3);
  to_vector(beta) ~ normal(0, 0.5);

  sigma_kappa ~ exponential(1);
  sigma_gamma ~ exponential(1);
  phi ~ gamma(10,1);

  for (n in 1:N) {
    real eta = alpha[age[n], sex[n]]
             + beta[age[n], sex[n]] * kappa[year[n]]
             + gamma[cohort[n], sex[n]];
    deaths[n] ~ neg_binomial_2_log(log(exposure[n]) + eta, phi);
  }
}
