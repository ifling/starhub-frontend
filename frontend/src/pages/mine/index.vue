<template>
  <view class="page">
    <text class="title">我的</text>
    <text class="desc">这里以后可以放“我的报名”、“个人信息”等内容。</text>
  </view>
</template>

<script>
export default {
  name: 'MinePage',
  data() {
    return {}
  },
}
</script>

<style>
.page {
  padding: 32rpx;
}

.title {
  font-size: 36rpx;
  font-weight: 600;
  margin-bottom: 16rpx;
}

.desc {
  font-size: 28rpx;
  color: #888;
}
</style>

