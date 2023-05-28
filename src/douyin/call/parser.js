const { match } = require('path-to-regexp');

const douyinHostRegexp = /www\.douyin\.com/i;
const douyinVideoRegexp = /\/(video|note)\/[0-9]+/i;
const douyinUserRegexp = /\/user\//i;
const videoIdRegexp = /^[0-9]+$/;
const douyinVideoUrlMatch = match('/(video|note)/:videoId');
const douyinUserUrlMatch = match('/user/:userId');
const douyinShareVideoUrlMatch = match('/share/(video|note)/:videoId');
const douyinShareUserUrlMatch = match('/share/user/:userId');

const DouyinUrlType = {
  Video: 'video',
  User: 'user'
};

function douyinShareVideoParse(pathname) {
  const matchResult = douyinShareVideoUrlMatch(pathname);

  if (typeof matchResult === 'object') {
    return {
      type: DouyinUrlType.Video,
      id: matchResult.params.videoId
    };
  }
}

function douyinShareUserParse(pathname) {
  const matchResult = douyinShareUserUrlMatch(pathname);

  if (typeof matchResult === 'object') {
    return {
      type: DouyinUrlType.User,
      id: matchResult.params.userId
    };
  }
}

/**
 * @param { string } url
 */
function parse(url) {
  let urlParseResult = null;

  try {
    urlParseResult = new URL(url);
  } catch { /* noop */ }

  if (!urlParseResult) {
    return {
      type: videoIdRegexp.test(url) ? DouyinUrlType.Video : DouyinUrlType.User,
      id: url
    };
  }

  const modalId = urlParseResult.searchParams.get('modal_id');

  if (modalId) {
    return {
      type: DouyinUrlType.Video,
      id: modalId
    };
  }

  if (douyinHostRegexp.test(urlParseResult.hostname) && douyinVideoRegexp.test(urlParseResult.pathname)) {
    const matchResult = douyinVideoUrlMatch(urlParseResult.pathname);

    return typeof matchResult === 'object' ? {
      type: DouyinUrlType.Video,
      id: matchResult.params.videoId
    } : undefined;
  }

  if (douyinHostRegexp.test(urlParseResult.hostname) && douyinUserRegexp.test(urlParseResult.pathname)) {
    const matchResult = douyinUserUrlMatch(urlParseResult.pathname);

    return typeof matchResult === 'object' ? {
      type: DouyinUrlType.User,
      id: matchResult.params.userId
    } : undefined;
  }
}