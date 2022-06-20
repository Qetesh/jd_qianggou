### 前置步骤：清空购物车，减少其他商品干扰
### 总体步骤如下：获取cookie->获取商品ID->设置抢购时间和数量->开始抢单

### 第一步：获取cookie
登录pc版JD商城，进入购物车，打开控制台，查看接口
https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart
的cookie，填入cookie的输入框

### 第二步：获取商品id
找到需要抢购的商品，查看详情，可以看到浏览器的URL为
https://item.jd.com/xxxxxxxx.html，
复制xxxxxxxx填入商品ID框，

### 第三步：设置抢购时间和数量
抢购时间需要格式设置，格式为yyyy-MM-dd HH:mm:ss，如2021-11-02 12:00:00。数量可随意设置，但需要考虑到店铺的库存以及是否设置为限购1件。

### 第四步：开始抢单
这个时候可以泡一杯茶，静待好事发生。

即可
 
**效果预览**

![](https://github.com/geeeeeeeek/jd_qianggou/blob/master/img/demo01.png)

**问题咨询**

微信：lengqin1024
