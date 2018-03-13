function a3(wd_coefficient, n_hid, n_iters, learning_rate, momentum_multiplier, do_early_stopping, mini_batch_size)
  % best: a3(0, 10, 70, 0.2, 0.9, false, 4)

  % wd coefficient classification validation loss:
  %  0      = 0.095000
  %  0.1    = 0.790000
  %  0.001  = 0.074000
  %  0.0001 = 0.092000

  % n hidden units to prevent overfitting
  % 10  = 0.370833
  % 30  = 0.286826
  % 100 = 0.090000
  % 130 = 0.091000

  % setup
  warning('error', 'Octave:broadcast');
  if exist('page_output_immediately');
    page_output_immediately(1);
  end
  more off;
  model = initial_model(n_hid);
  from_data_file = load('data.mat');
  datas = from_data_file.data;
  n_training_cases = size(datas.training.inputs, 2);

  if n_iters ~= 0;
    test_gradient(model, datas.training, wd_coefficient)
  end

  % optimization
  theta = model_to_theta(model);
  momentum_speed = theta * 0;
  training_data_losses = [];
  validation_data_losses = [];
  if do_early_stopping,
    best_so_far.theta = -1; % this will be overwritten soon
    best_so_far.validation_loss = inf;
    best_so_far.after_n_iters = -1;
  end
  for optimization_iteration_i = 1:n_iters,
    model = theta_to_model(theta);

    training_batch_start = mod((optimization_iteration_i-1) * mini_batch_size, n_training_cases)+1;
    training_batch.inputs = datas.training.inputs(:, training_batch_start : training_batch_start + mini_batch_size - 1);
    training_batch.targets = datas.training.targets(:, training_batch_start : training_batch_start + mini_batch_size - 1);
    gradient = model_to_theta(d_loss_by_d_model(model, training_batch, wd_coefficient));
    momentum_speed = momentum_speed * momentum_multiplier - gradient;
    theta = theta + momentum_speed * learning_rate;

    model = theta_to_model(theta);
    training_data_losses = [training_data_losses, loss(model, datas.training, wd_coefficient)];
    validation_data_losses = [validation_data_losses, loss(model, datas.validation, wd_coefficient)];

    if do_early_stopping && validation_data_losses(end) < best_so_far.validation_loss,
      best_so_far.theta = theta; % this will be overwritten soon
      best_so_far.validation_loss = validation_data_losses(end);
      best_so_far.after_n_iters = optimization_iteration_i;
    end

    if mod(optimization_iteration_i, round(n_iters/10)) == 0,
      fprintf('After %d optimization iterations, training data loss is %f, and validation data loss is %f\n', ...
        optimization_iteration_i, training_data_losses(end), validation_data_losses(end));
    end
  end

  % test gradient again with typical parameters
  if n_iters ~= 0;
    test_gradient(model, datas.training, wd_coefficient);
  end

  if do_early_stopping;
    fprintf('Early stopping: validation loss min after %d iter. chose that model.\n', best_so_far.after_n_iters);
    theta = best_so_far.theta;
  end

  % the optimization is finished. Now do some reporting.
  model = theta_to_model(theta);
  if n_iters ~= 0,
    clf;
    hold on;
    plot(training_data_losses, 'b');
    plot(validation_data_losses, 'r');
    legend('training', 'validation');
    ylabel('loss');
    xlabel('iteration number');
    hold off;
  end

  datas2 = {datas.training, datas.validation, datas.test};
  data_names = {'training', 'validation', 'test'};

  for data_i = 1:3,
    data = datas2{data_i};
    data_name = data_names{data_i};
    fprintf('\nThe loss on the %s data is %f\n', data_name, loss(model, data, wd_coefficient));
    if wd_coefficient~=0,
      fprintf('The classification loss (i.e. without weight decay) on the %s data is %f\n', ...
        data_name, loss(model, data, 0));
    end
    fprintf('The classification error rate on the %s data is %f\n', ...
      data_name, classification_performance(model, data));
  end
end

function test_gradient(model, data, wd_coefficient)
  base_theta = model_to_theta(model);
  h = 1e-2;
  correctness_threshold = 1e-5;
  analytic_gradient = model_to_theta(d_loss_by_d_model(model, data, wd_coefficient));

  % test the gradient for a few elements of theta for efficiency
  for i = 1:100,
    % 1299721 is prime and thus ensures a somewhat random-like selection of indices
    test_index = mod(i * 1299721, size(base_theta,1)) + 1;
    analytic_here = analytic_gradient(test_index);
    theta_step = base_theta * 0;
    theta_step(test_index) = h;
    contribution_distances = [-4:-1, 1:4];
    contribution_weights = [1/280, -4/105, 1/5, -4/5, 4/5, -1/5, 4/105, -1/280];
    temp = 0;
    for contribution_index = 1:8,
      temp = temp + loss(theta_to_model(base_theta + theta_step * contribution_distances(contribution_index)), data, wd_coefficient) * contribution_weights(contribution_index);
    end
    fd_here = temp / h;
    diff = abs(analytic_here - fd_here);
    % fprintf('%d %e %e %e %e\n', test_index, base_theta(test_index), diff, fd_here, analytic_here);

    % check delta between analytic gradient and finite difference gradient
    if diff < correctness_threshold;
      continue;
    end
    if diff / (abs(analytic_here) + abs(fd_here)) < correctness_threshold;
      continue;
    end

    error(sprintf('theta element=#%d, value=%e, finite difference gradient=%e, analytic gradient=%e.\n', ...
      test_index, base_theta(test_index), fd_here, analytic_here));
  end
  fprintf('analytic gradient is within 0.001%% of finite difference gradient.\n');
end

function ret = logistic(input)
  ret = 1 ./ (1 + exp(-input));
end

function ret = log_sum_exp_over_rows(a)
  % This computes log(sum(exp(a), 1)) in a numerically stable way
  maxs_small = max(a, [], 1);
  maxs_big = repmat(maxs_small, [size(a, 1), 1]);
  ret = log(sum(exp(a - maxs_big), 1)) + maxs_small;
end

function ret = loss(model, data, wd_coefficient)
  % model.input_to_hid:
  %     matrix of size <number of hidden units> by <number of inputs i.e. 256>
  %     contains the weights from the input units to the hidden units
  % model.hid_to_class:
  %     matrix of size <number of classes i.e. 10> by <number of hidden units>
  %     contains the weights from the hidden units to the softmax units
  % data.inputs:
  %     matrix of size <number of inputs i.e. 256> by <number of data cases>
  %     each column describes a different data case
  % data.targets:
  %     matrix of size <number of classes i.e. 10> by <number of data cases>
  %     each column describes a different data case. It contains a one-of-N
  %     encoding of the class, (one element in every column is 1 and rest are 0)
  %
  % before calculating loss, need to calculate a variety of intermediate values,
  % like the state of the hidden units.

  % input to the hidden units, i.e. before the logistic.
  % size: <number of hidden units> by <number of data cases>
  hid_input = model.input_to_hid * data.inputs;

  % output of the hidden units, i.e. after the logistic.
  % size: <number of hidden units> by <number of data cases>
  hid_output = logistic(hid_input);

  % input to the components of the softmax.
  % size: <number of classes, i.e. 10> by <number of data cases>
  class_input = model.hid_to_class * hid_output;

  % softmax implementation differs from lectures. instead of using an
  % exponential divided by a sum of exponentials, we do something exactly the
  % same while avoiding very large numbers, which makes the code numerically
  % stable (e.g., 10^1000).

  % log(sum(exp of class_input)) is what we subtract to get properly normalized log class probabilities.
  % size: <1> by <number of data cases>
  class_normalizer = log_sum_exp_over_rows(class_input);

  % log of probability of each class.
  % size: <number of classes, i.e. 10> by <number of data cases>
  log_class_prob = class_input - repmat(class_normalizer, [size(class_input, 1), 1]);

  % probability of each class. each column (i.e. each case) sums to 1.
  % size: <number of classes, i.e. 10> by <number of data cases>
  class_prob = exp(log_class_prob);

  % select the right log class probability using that sum; then take mean over all data cases.
  classification_loss = -mean(sum(log_class_prob .* data.targets, 1));

  % weight decay loss. very straightforward: E = 1/2 * wd_coeffecient * theta^2
  wd_loss = sum(model_to_theta(model).^2)/2*wd_coefficient;

  ret = classification_loss + wd_loss;
end

function ret = d_loss_by_d_model(model, data, wd_coefficient)
  % ONLY FUNCTION TO EDIT
  %
  % model.input_to_hid:
  %     matrix size: <number of hidden units> by <number of inputs i.e. 256>
  % model.hid_to_class:
  %     matrix size: <number of classes i.e. 10> by <number of hidden units>
  % data.inputs:
  %     matrix size: <number of inputs i.e. 256> by <number of data cases>
  %     each column describes a different data case.
  % data.targets:
  %     matrix size: <number of classes i.e. 10> by <number of data cases>.
  %     each column describes a different data case.
  %     contains a one-of-N encoding of the class, i.e. one element in every
  %     column is 1 and the others are 0.
  %
  % returned object is supposed to be exactly like parameter <model>, i.e. it
  % has fields ret.input_to_hid and ret.hid_to_class. However, the contents of
  % those matrices are gradients (d loss by d model parameter), instead of model
  % parameters.

  hid_input = model.input_to_hid * data.inputs;
  hid_output = logistic(hid_input);
  class_input = model.hid_to_class * hid_output;
  class_normalizer = log_sum_exp_over_rows(class_input);
  log_class_prob = class_input - repmat(class_normalizer, [size(class_input, 1), 1]);
  class_prob = exp(log_class_prob);
  classification_loss = -mean(sum(log_class_prob .* data.targets, 1));
  wd_loss = sum(model_to_theta(model).^2)/2*wd_coefficient;

  % lecture 3 c
  ret.input_to_hid = (model.hid_to_class' * (class_prob - data.targets) .* hid_output .* (1 - hid_output) * data.inputs') / size(hid_output, 2) + wd_coefficient * model.input_to_hid;
  ret.hid_to_class = (class_prob - data.targets) * hid_output' / size(hid_output, 2) + wd_coefficient * model.hid_to_class;
end

% takes a model (or gradient in model form), and turns it into one long vector.
% also see theta_to_model.
function ret = model_to_theta(model)
  input_to_hid_transpose = transpose(model.input_to_hid);
  hid_to_class_transpose = transpose(model.hid_to_class);
  ret = [input_to_hid_transpose(:); hid_to_class_transpose(:)];
end

% Takes a model (or gradient) in the form of one long vector i (maybe produced
% by model_to_theta), and restores it to the structure format, i.e. with fields
% .input_to_hid and .hid_to_class, both matrices.
function ret = theta_to_model(theta)
  n_hid = size(theta, 1) / (256+10);
  ret.input_to_hid = transpose(reshape(theta(1: 256*n_hid), 256, n_hid));
  ret.hid_to_class = reshape(theta(256 * n_hid + 1 : size(theta,1)), n_hid, 10).';
end

function ret = initial_model(n_hid)
  n_params = (256+10) * n_hid;
  as_row_vector = cos(0:(n_params-1));
  % no random initialization so everybody gets same results.
  ret = theta_to_model(as_row_vector(:) * 0.1);
end

% returns the fraction of data cases that is incorrectly classified by the model.
function ret = classification_performance(model, data)
  % input to the hidden units, i.e. before logistic
  % size: <number of hidden units> by <number of data cases>
  hid_input = model.input_to_hid * data.inputs;

  % output of the hidden units, i.e. after the logistic
  % size: <number of hidden units> by <number of data cases>
  hid_output = logistic(hid_input);

  % input to the components of the softmax
  % size: <number of classes, i.e. 10> by <number of data cases>
  class_input = model.hid_to_class * hid_output;

  [dump, choices] = max(class_input); % choices is integer: the chosen class, plus 1.
  [dump, targets] = max(data.targets); % targets is integer: the target class, plus 1.
  ret = mean(double(choices ~= targets));
end

