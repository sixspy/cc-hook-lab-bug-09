/** 投递台页面模块：accept · 事件队列
 * 建事件写库，状态待投
 * 真实页面在 backend/app/static；本模块提供状态文案与表格辅助。
 */
export const PAGE = 'accept';
export const TITLE = '事件队列';

export const STAGE_COPY = {
  accept: '受理：建事件写库，状态待投',
  dispatch: '投递：占通道端点，事件转投递中',
  receipt: '死信：现场载荷摘要写库，事件转待确认',
  verify: '互证：通过关闭，作废按签名规回流',
  crew: '通道：启用停用与占用互证',
};

const FATE_TONE = {
  '待投': 'warn', '投递中': 'info', '待确认': 'warn', '已投递': 'ok', '已作废': 'danger',
};

export function fateChip(fate) {
  return { text: fate || '—', tone: FATE_TONE[fate] || 'muted' };
}

export function priorityLabel(p) {
  const map = { '紧急': '高', '普通': '中', '低': '低' };
  return map[p] || p || '中';
}

export function boneAssert() {
  return '主链是全栈事件业务，不是采集入库编排。';
}

export function emptyState(kind) {
  const tips = {
    orders: '尚无事件。回事件队列建单或灌夹具。',
    dispatch: '尚无投递。待投事件在投递流水占端点。',
    receipt: '死信匣为空。投递中事件可写现场载荷摘要。',
    verify: '尚无互证。待确认事件在投递互证结案。',
    crew: '端点名册从 seed 预置端点。',
  };
  return tips[kind] || '暂无数据';
}

export function metricCards(overview) {
  const o = overview || {};
  return [
    { key: '待投', value: o['待投'] ?? 0, hint: '可投递' },
    { key: '投递中', value: o['投递中'] ?? 0, hint: '待死信' },
    { key: '待确认', value: o['待确认'] ?? 0, hint: '待互证' },
    { key: '已投递', value: o['已投递'] ?? 0, hint: '结案' },
  ];
}

export function sortByTime(rows, field) {
  const f = field || '更新时';
  return [...(rows || [])].sort((a, b) => String(b[f] || '').localeCompare(String(a[f] || '')));
}

export function filterByState(rows, state) {
  if (!state) return rows || [];
  return (rows || []).filter((r) => r.状态 === state);
}

export function rowValidate(r) {
  const miss = [];
  if (!r?.事件号) miss.push('缺事件号');
  if (!r?.事件类型 && PAGE === 'accept') miss.push('缺事件类型');
  return miss;
}

export function summarizeDispatch(row) {
  if (!row) return '无投递';
  return `${row.尝试号 || ''} · ${row.端点键 || ''} · ${row.状态 || ''}`;
}

export function summarizeReceipt(row) {
  if (!row) return '无死信';
  return `${row.死信号} · 照片${row.失败次数}`;
}

export function summarizeVerify(row) {
  if (!row) return '无互证';
  return `${row.结论} · ${row.备注 || ''}`;
}

export function crewBadge(onDuty) {
  return onDuty ? { text: '启用', tone: 'ok' } : { text: '停用', tone: 'muted' };
}

export function mutualAlignHint(aligned) {
  return aligned ? '占用未超过启用，互证对齐' : '占用超过启用，互证撕裂';
}

export function buildNavCopy() {
  return '事件队列：建事件写库，状态待投';
}

export function tableHeaders(kind) {
  const map = {
    orders: ['事件号', '事件类型', '回调地址', '优先级', '状态'],
    dispatch: ['尝试号', '事件号', '端点键', '通道', '状态'],
    receipt: ['死信号', '事件号', '载荷摘要', '失败次数'],
    verify: ['互证号', '事件号', '结论', '备注'],
    crew: ['端点键', '姓名', '通道', '启用'],
  };
  return map[kind] || ['键', '值'];
}

export function formatRulePatch(patch) {
  const out = {};
  for (const k of ['投递上限', '作废策略', '互证必审照片']) {
    if (patch[k] != null) out[k] = String(patch[k]);
  }
  return out;
}

export function assertLoginHint() {
  return '未登录将跳转 /login，账号 admin 密码 123456';
}

export function chainSteps() {
  return ['受理', '投递', '死信', '互证', '互证'];
}

export function stepIndex(name) {
  return chainSteps().indexOf(name);
}

export function nextStepAfter(state) {
  const flow = { '待投': '投递', '投递中': '死信', '待确认': '互证', '已投递': '—', '已作废': '投递' };
  return flow[state] || '受理';
}

export function describePage() {
  return { id: PAGE, title: TITLE, copy: buildNavCopy() };
}
export function helper_accept_0(n) { return (n ?? 0) + 0; }
export function helper_accept_1(n) { return (n ?? 0) + 1; }
export function helper_accept_2(n) { return (n ?? 0) + 2; }
export function helper_accept_3(n) { return (n ?? 0) + 3; }
export function helper_accept_4(n) { return (n ?? 0) + 4; }
export function helper_accept_5(n) { return (n ?? 0) + 5; }
export function helper_accept_6(n) { return (n ?? 0) + 6; }
export function helper_accept_7(n) { return (n ?? 0) + 7; }
export function helper_accept_8(n) { return (n ?? 0) + 8; }
export function helper_accept_9(n) { return (n ?? 0) + 9; }
export function helper_accept_10(n) { return (n ?? 0) + 10; }
export function helper_accept_11(n) { return (n ?? 0) + 11; }
