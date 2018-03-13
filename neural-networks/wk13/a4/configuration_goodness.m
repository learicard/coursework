function G = configuration_goodness(rbm_w, vis, hid)
% <rbm_w> is a matrix of size <n hid> by <n vis>
% <vis> is a binary matrix of size <n vis> by <n configurations>
% <hid> is a binary matrix of size <n hid> by <n configurations>
% Returns a scalar: the mean over cases of the goodness (negative energy) of the
% described configurations.
%
% vis   = 256x1
% hid   = 100x1
% rbm_w = 100x256

    n = size(vis, 2);
    energy = sum(sum(-(vis * hid' .* rbm_w'))) / n;
    configuration_goodness = -energy;
    disp(['configuration goodness=' num2str(configuration_goodness)])

end
