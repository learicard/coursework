function d_G_by_rbm_w = configuration_goodness_gradient(vis, hid)
% <vis> is a binary matrix of size <n vis> by <n configurations>.
% <hid> is a (possibly but not necessarily binary) matrix of size <n hid> by <n configurations>.
%
% You don't need the model parameters for this computation.
% This returns the gradient of the mean configuration goodness (negative energy,
% as computed by function <configuration_goodness>) with respect to the model
% parameters. Thus, the returned value is of the same shape as the model
% parameters, which by the way are not provided to this function. Notice that
% we're talking about the mean over data cases (as opposed to the sum over data cases).

    n = size(vis, 2);
    d_G_by_rbm_w = hid * vis'  / n;

end
