% This function returns line indexes that gives marginal impact below 340
% GHz, compared to using all MPM lines.

function i_lines = select_mpm_lines

% Exclude lines with these indexes
exclude = [2:3 9:10 14:18 20:21 23:29];

i_lines = setdiff( 1:30, exclude );