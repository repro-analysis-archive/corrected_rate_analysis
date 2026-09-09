function out = jiim_wrap_r7(labels, maxchar)
% Wrap long row labels, preferring " + " joins and falling back to spaces.
% Each output element is either a char or a cellstr of lines. The lines always
% rejoin to the exact canonical string (asserted by jiim_wrap_check_r7).
if nargin < 2, maxchar = 22; end
out = cell(size(labels));
for i = 1:numel(labels)
    s = strtrim(labels{i});
    if numel(s) <= maxchar, out{i} = s; continue; end
    if contains(s,' + ')
        parts = strsplit(s,' + '); joiner = ' + '; cont = '+ ';
    else
        parts = strsplit(s,' ');   joiner = ' ';   cont = '';
    end
    lines = {}; cur = parts{1};
    for k = 2:numel(parts)
        cand = [cur joiner parts{k}];
        if numel(cand) <= maxchar
            cur = cand;
        else
            lines{end+1} = cur;                %#ok<AGROW>
            cur = [cont parts{k}];
        end
    end
    lines{end+1} = cur;                        %#ok<AGROW>
    out{i} = lines;
end
end
