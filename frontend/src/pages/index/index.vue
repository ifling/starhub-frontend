<template>
  <view class="page">
    <view class="section-header">
      <text class="section-title">工具</text>
    </view>
    <view class="section-divider"></view>

    <view class="tool-list">
      <view class="tool-item" @click="onClickStone">
        <view class="tool-icon" hover-class="tool-icon--hover" hover-stay-time="80">
          <view class="tool-icon__glyph"></view>
        </view>
        <text class="tool-name">组队</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    onClickStone() {
      uni.navigateTo({
        url: '/pages/stone/index',
      })
    },
  },
}
</script>

<style>
.page {
  padding: 32rpx;
  background: #f6f7fb;
  min-height: 100vh;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
}

.section-header {
  margin-bottom: 16rpx;
}

.section-divider {
  height: 2rpx;
  background-color: rgba(0, 0, 0, 0.08);
  margin-bottom: 24rpx;
}

.tool-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 24rpx;
  justify-content: flex-start;
  align-items: flex-start;
}

.tool-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.tool-icon {
  width: 120rpx;
  height: 120rpx;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-icon--hover {
  transform: scale(0.98);
  opacity: 0.92;
}

.tool-icon__glyph {
  width: 120rpx;
  height: 120rpx;
  background-image: url('/static/icons/stone.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.tool-name {
  font-size: 26rpx;
  margin-top: 8rpx;
  color: #111827;
}
</style>

