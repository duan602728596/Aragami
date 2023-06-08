import http from 'node:http';
import { setTimeout as setTimeoutPromise } from 'node:timers/promises';
import { spawn } from 'node:child_process';
import Koa from 'koa';
import Router from '@koa/router';
import { koaBody } from 'koa-body';
import CDP from 'chrome-remote-interface';

let child;
let client;

async function command(cmd, args) {
  if (!child) {
    child = spawn(cmd, args, { stdio: 'inherit' });

    child.on('close', function(code) {
      child = null;
    });

    child.on('error', function(error) {
      child = null;
    });

    await setTimeoutPromise(5_000);
  }
}

async function clientSwitch() {
  if (client) {
    const { targetInfos } = await client.Target.getTargets();
    const xiaohongshuTarget = targetInfos.find(
      (target) => target.type === 'page' && target.url.includes('www.xiaohongshu.com'));

    if (xiaohongshuTarget && !xiaohongshuTarget.attached) {
      await client.Target.attachToTarget({ targetId: xiaohongshuTarget.targetId });
    }
  }
}

const app = new Koa();
const router = new Router();

app.use(koaBody());
app.use(router.routes())
  .use(router.allowedMethods());

router.post('/api/init', async function(ctx, next) {
  const { port, executablePath } = ctx.request.body;

  if (!(port && executablePath)) {
    ctx.status = 400;
    ctx.body = { success: false };
    await next();

    return;
  }

  if (!client) {
    await command(executablePath, [`--remote-debugging-port=${ port }`, '--disable-gpu']);
    client = await CDP({ port });
    await Promise.all([
      client.Page.enable(),
      client.Network.enable(),
      client.Runtime.enable()
    ]);
    await client.Page.navigate({ url: 'https://www.xiaohongshu.com/user/profile/594099df82ec393174227f18' });
    await client.Page.loadEventFired();
    await setTimeoutPromise(3_000);
  }

  ctx.status = 200;
  ctx.body = { success: true };
});

router.post('/api/sign', async function(ctx, next) {
  const { url, data } = ctx.request.body;

  if (!client) {
    ctx.status = 400;
    ctx.body = { success: false };
    await next();

    return;
  }

  await clientSwitch();

  const signResult = await client.Runtime.evaluate({
    expression: `JSON.stringify(window._webmsxyw("${ url }", ${ data ?? 'undefined' }));`
  });

  ctx.status = 200;
  ctx.body = {
    success: true,
    data: JSON.parse(signResult.result.value)
  };
  await next();
});

router.post('/api/cookie', async function(ctx, next) {
  if (!client) {
    ctx.status = 400;
    ctx.body = { success: false };
    await next();

    return;
  }

  await clientSwitch();

  const cookies = (await client.Network.getCookies()).cookies.map((cookie) => `${ cookie.name }=${ cookie.value }`).join('; ');

  ctx.status = 200;
  ctx.body = {
    success: true,
    data: cookies
  };
  await next();
});

http.createServer(app.callback()).listen(32_000);