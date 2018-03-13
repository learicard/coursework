function ret = cd1(rbm_w, vis_data)
% <rbm_w> is a matrix of size <n hid> by <n vis>
% <vis_data> is a (possibly but not necessarily binary) matrix of size <n vis>
% by <n data cases>
%
% The returned value is the gradient approximation produced by CD-1. It's of the
% same shape as <rbm_w>.

    n = size(vis_data, 2);

    % sample from data
    vis_data = sample_bernoulli(vis_data);

    % generate fake data from the hidden layer
    hid_prob = logistic(rbm_w * vis_data);
    hid_data = sample_bernoulli(hid_prob);

    % compute gradient between hidden layer and visible layer
    grad0 = hid_data * vis_data';

    % generate reconstruction of vis_data, sample
    v1_prob = logistic(rbm_w' * hid_data);
    reconstruction = sample_bernoulli(v1_prob);

    % recompute fake data from the hidden layer
    hid_prob = logistic(rbm_w * reconstruction);
    %hid_data = sample_bernoulli(hid_prob);

    % compute gradient between hidden layer data and reconstruction
    %grad1 = hid_data * reconstruction';
    grad1 = hid_prob * reconstruction';

    % sampling the hidden state that results from the "reconstruction" visible
    % state is useless: it does not change theexpected value of the gradient
    % estimate that CD-1 produces; it only increases its variance.

    ret = (grad0-grad1)/n;

end
