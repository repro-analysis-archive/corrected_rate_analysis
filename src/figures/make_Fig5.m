% make_Fig5.m — Q4: (A) A/D1/D2/B preprocessing-placement matrix, (B) half-specific B-A,
% (C) pooled additive P / S / P x S contrasts. Reference = 0. Descriptive: no interval,
% no p-value, no ratio, no exponentiation. Class V.
% Panels B and C measure DIFFERENT quantities, so each carries its own x label and they are
% given EQUAL physical width (v9 section 5-B); one shared row-label column serves both.
S = jiim_style_r7();
here = fileparts(mfilename('fullpath'));
D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
outdir = fullfile(here,'..','..','reproduction','figures');

bH1=D.f5b_H1(:); bH2=D.f5b_H2(:);
cP=D.f5c_P(:); cS=D.f5c_S(:); cPS=D.f5c_PS(:);
pNA=logical(D.f5c_P_isNA(:)); sNA=logical(D.f5c_PS_isNA(:));
labs=cellstr(D.labels); n=numel(bH1);
assert(sum(sign(bH1).*sign(bH2)<0)==6,'Fig5B: sign disagreement must hold in all six rows');
assert(pNA(1) && sNA(1) && isnan(cP(1)) && isnan(cPS(1)),'Fig5C: clinical-only P/PxS must be N/A');

fig = figure('Color',[1 1 1],'Units','centimeters','Position',[2 2 S.width_cm 14.4]);
fsm = S.ftick-2;

% ================= Panel A — placement matrix (native vector) =================
axA = axes('Parent',fig,'Units','normalized','Position',[0.055 0.760 0.915 0.190]);
hold(axA,'on'); axis(axA,[0 1 0 1]); axis(axA,'off');
rg  = {'A','D1','D2','B'};
Pf  = [0 1 0 1];      % imaging block (scaling + PCA) fitted on the full 739
Sf  = [0 0 1 1];      % clinical scaler fitted on the full 739
cx  = [0.335 0.505 0.675 0.845];
rectangle(axA,'Position',[0.245 0.270 0.700 0.520],'Curvature',0.10, ...
          'EdgeColor',S.softedge,'LineWidth',0.9,'FaceColor',[0.979 0.979 0.979]);
for k=1:4
    text(axA,cx(k),0.960,rg{k},'FontName','Arial','FontWeight','bold','FontSize',S.ftick, ...
         'HorizontalAlignment','center','Color',S.text,'Interpreter','none');
end
text(axA,0.215,0.660,'P','FontName','Arial','FontWeight','bold','FontSize',S.ftick, ...
     'HorizontalAlignment','right','Color',S.text,'Interpreter','none');
text(axA,0.215,0.400,'S','FontName','Arial','FontWeight','bold','FontSize',S.ftick, ...
     'HorizontalAlignment','right','Color',S.text,'Interpreter','none');
for k=1:4
    mk_(axA,cx(k),0.660,Pf(k),S);
    mk_(axA,cx(k),0.400,Sf(k),S);
end
% key + the invariant, both outside every data region
mk_(axA,0.290,0.155,1,S);
text(axA,0.320,0.155,'full n = 739','FontName','Arial','FontSize',fsm, ...
     'HorizontalAlignment','left','Color',S.text,'Interpreter','none');
mk_(axA,0.560,0.155,0,S);
text(axA,0.590,0.155,'training half','FontName','Arial','FontSize',fsm, ...
     'HorizontalAlignment','left','Color',S.text,'Interpreter','none');
% Balanced between the key row above and the (B)/(C) region below: measured at the final 174 mm
% width the free band is 8.88 mm, so y = -0.073 (2.95 mm below the previous position) leaves
% 2.00 mm clear of the key row and 2.65 mm clear of the panel labels. The coordinate is below the
% axis box, which is why Clipping is off; panel A's axes Position is untouched so that A/D1/D2/B,
% the regime box and the key row all keep their exact previous figure positions.
text(axA,0.030,-0.073,'CATE model: opposite-half training in all regimes', ...
     'FontName','Arial','FontSize',fsm,'HorizontalAlignment','left','Color',S.text, ...
     'Interpreter','none','Clipping','off');

% ================= Panels B and C — equal physical width =================
y = n:-1:1; off = 0.185;
axB = axes('Parent',fig,'Units','normalized','Position',[0.310 0.200 0.280 0.450]);
hold(axB,'on');
xline(axB,0,':','Color',S.zero,'LineWidth',1.0);
for i=1:n
    plot(axB,[bH1(i) bH2(i)],[y(i)+off y(i)-off],'-','Color',S.conn,'LineWidth',1.1);
end
b1 = plot(axB,bH1,y+off,'o','MarkerSize',S.mk_open,'MarkerFaceColor','none', ...
          'MarkerEdgeColor',S.dark,'LineWidth',S.mk_edge,'LineStyle','none');
b2 = plot(axB,bH2,y-off,'^','MarkerSize',S.mk_open,'MarkerFaceColor','none', ...
          'MarkerEdgeColor',S.medium,'LineWidth',S.mk_edge,'LineStyle','none');
set(axB,'YLim',[0.40 n+0.60]); xlim(axB,[-0.125 0.125]);
set(axB,'XTick',[-0.10 0 0.10],'XTickLabel',{'-0.10','0','0.10'},'XTickLabelRotation',0);
xlabel(axB,'Change in RATE (B − A)','FontName','Arial','FontSize',S.ftick, ...
       'Color',S.text,'Interpreter','none');
jiim_axes_r7(axB,S);
% three panels leave a narrower label column here, so the shared row labels are set at
% 13 pt (well above the 7 pt floor) rather than wrapping to three lines and colliding.
jiim_ylabels_r7(axB,y,labs,S,22,13);           % one shared label column for both panels

axC = axes('Parent',fig,'Units','normalized','Position',[0.680 0.200 0.280 0.450]);
hold(axC,'on'); dy = 0.205;
xline(axC,0,':','Color',S.zero,'LineWidth',1.0);
mP = ~isnan(cP); mPS = ~isnan(cPS);
hP = plot(axC,cP(mP),y(mP)+dy,'o','MarkerSize',S.mk_fill,'MarkerFaceColor',S.navy, ...
          'MarkerEdgeColor',S.text,'LineWidth',S.mk_edge,'LineStyle','none');
hS = plot(axC,cS,y,'o','MarkerSize',S.mk_open,'MarkerFaceColor','none', ...
          'MarkerEdgeColor',S.dark,'LineWidth',S.mk_edge,'LineStyle','none');
hPS = plot(axC,cPS(mPS),y(mPS)-dy,'^','MarkerSize',S.mk_open,'MarkerFaceColor','none', ...
           'MarkerEdgeColor',S.medium,'LineWidth',S.mk_edge,'LineStyle','none');
set(axC,'YLim',[0.40 n+0.60]); xlim(axC,[-0.052 0.052]);
set(axC,'XTick',[-0.04 0 0.04],'XTickLabel',{'-0.04','0','0.04'},'XTickLabelRotation',0);
xlabel(axC,'Pooled change in RATE','FontName','Arial','FontSize',S.ftick, ...
       'Color',S.text,'Interpreter','none');
jiim_axes_r7(axC,S); set(axC,'YTick',[]);

% legends: generated from the ACTIVE handles, each directly above its own panel
hsB=[b1 b2]; nmB={sprintf('H1 (n = %d)',D.nH1), sprintf('H2 (n = %d)',D.nH2)};
kB = arrayfun(@(g) ~isempty(get(g,'XData')) && any(~isnan(get(g,'XData'))), hsB);
lgB = legend(axB,hsB(kB),nmB(kB),'Orientation','horizontal','FontName','Arial', ...
             'FontSize',fsm,'Box','off','TextColor',S.text,'Interpreter','none');
lgB.Units='normalized'; lgB.Position=[0.300 0.664 0.275 0.040];
hsC=[]; nmC={};
if any(mP),  hsC=[hsC hP];  nmC{end+1}='P';     end
hsC=[hsC hS]; nmC{end+1}='S';
if any(mPS), hsC=[hsC hPS]; nmC{end+1}='P × S'; end
lgC = legend(axC,hsC,nmC,'Orientation','horizontal','FontName','Arial', ...
             'FontSize',fsm,'Box','off','TextColor',S.text,'Interpreter','none');
lgC.Units='normalized'; lgC.Position=[0.678 0.664 0.275 0.040];

% long definitions kept out of every data region (v9 section 5-C)
annotation(fig,'textbox',[0.055 0.008 0.930 0.070], ...
  'String',{'P, imaging-block preprocessing placement (scaling + PCA)', ...
            'S, clinical-scaler placement'}, ...
  'FontName','Arial','FontSize',fsm,'EdgeColor','none','Color',S.text, ...
  'HorizontalAlignment','left','VerticalAlignment','middle','FitBoxToText','off', ...
  'Interpreter','none');
annotation(fig,'textbox',[0.014 0.940 0.06 0.05],'String','(A)','FontName','Arial','FontWeight','bold', ...
  'FontSize',S.fpanel,'EdgeColor','none','Color',S.text,'FitBoxToText','on');
annotation(fig,'textbox',[0.014 0.678 0.06 0.05],'String','(B)','FontName','Arial','FontWeight','bold', ...
  'FontSize',S.fpanel,'EdgeColor','none','Color',S.text,'FitBoxToText','on');
annotation(fig,'textbox',[0.600 0.678 0.06 0.05],'String','(C)','FontName','Arial','FontWeight','bold', ...
  'FontSize',S.fpanel,'EdgeColor','none','Color',S.text,'FitBoxToText','on');
jiim_export_r7(fig,'Fig5',outdir);

function mk_(ax,x,yy,full,S)
% filled navy square = fitted on the full n = 739; open dark-gray square = training half
if full
    plot(ax,x,yy,'s','MarkerSize',7.0,'MarkerFaceColor',S.navy, ...
         'MarkerEdgeColor',S.text,'LineWidth',0.8,'LineStyle','none');
else
    plot(ax,x,yy,'s','MarkerSize',7.0,'MarkerFaceColor','none', ...
         'MarkerEdgeColor',S.dark,'LineWidth',0.9,'LineStyle','none');
end
end
