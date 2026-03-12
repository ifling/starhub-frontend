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
        <text class="tool-name">集合石</text>
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
  width: 140rpx;
  height: 140rpx;
  padding: 0;
  border-radius: 28rpx;
  background: linear-gradient(135deg, #34d399 0%, #10b981 55%, #059669 100%);
  box-shadow: 0 14rpx 34rpx rgba(16, 185, 129, 0.28);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-icon--hover {
  transform: scale(0.98);
  opacity: 0.92;
}

.tool-icon__glyph {
  width: 56rpx;
  height: 56rpx;
  border-radius: 18rpx;
  background: rgba(255, 255, 255, 0.92);
}

.tool-name {
  font-size: 26rpx;
  margin-top: 8rpx;
  color: #111827;
}
</style>

