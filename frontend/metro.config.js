const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const projectRoot = __dirname;
const config = getDefaultConfig(projectRoot);

// 1. shared 폴더의 절대 경로 계산
// const sharedPath = path.resolve(projectRoot, '../shared');

const workspaceRoot  = path.resolve(projectRoot, '..');

// 2. Metro가 감시할 폴더 리스트에 shared 추가
config.watchFolders = [workspaceRoot];

// 3. shared 내부의 모듈을 찾을 수 있도록 설정
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
];

module.exports = config;
