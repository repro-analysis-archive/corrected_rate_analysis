function jiim_wrap_check_r7(orig, wrapped)
% Assert every wrapped label rejoins to its exact canonical string.
for i = 1:numel(orig)
    w = wrapped{i};
    if ischar(w), j = w; else
        j = w{1};
        for k = 2:numel(w)
            nx = w{k};
            if startsWith(nx,'+ '), j = [j ' ' nx]; else, j = [j ' ' nx]; end %#ok<AGROW>
        end
    end
    assert(strcmp(j, orig{i}), 'wrap rejoin failed: "%s" != "%s"', j, orig{i});
end
end
