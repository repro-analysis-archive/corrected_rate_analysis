function jiim_ylabels_r7(ax, yvals, labels, S, maxchar, fsz)
% Right-aligned, possibly multi-line row labels drawn as text objects.
% MATLAB YTickLabel cannot hold multi-line cells, so tick labels are cleared and
% the labels are drawn explicitly. Interpreter 'none' throughout.
if nargin < 5 || isempty(maxchar), maxchar = 22; end
if nargin < 6 || isempty(fsz), fsz = S.ftick; end
w = jiim_wrap_r7(labels, maxchar);
jiim_wrap_check_r7(labels, w);
set(ax,'YTick',[]);
xl = get(ax,'XLim'); pad = 0.035*diff(xl);
for i = 1:numel(yvals)
    text(ax, xl(1)-pad, yvals(i), w{i}, 'FontName','Arial','FontSize',fsz, ...
        'Color',S.text,'HorizontalAlignment','right','VerticalAlignment','middle', ...
        'Interpreter','none','Clipping','off');
end
end
