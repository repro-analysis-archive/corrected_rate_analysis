% Clean rebuild of the whole R7 final figure round from canonical data + the .m files.
close all force; clear; clc;
here = fileparts(mfilename('fullpath')); cd(here); addpath(here);
assert(any(strcmpi(listfonts,'Arial')), 'Arial is not available; stop before rendering.');
for k = 1:5
    fprintf('--- Fig%d ---\n', k);
    run(fullfile(here, sprintf('make_Fig%d.m', k)));
    close all force;
end
fprintf('build_all complete\n');
