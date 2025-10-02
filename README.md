
import React, { useState } from 'react';
import { Shield, AlertTriangle, CheckCircle, Mail, Link } from 'lucide-react';

export default function PhishingChecker() {
  const [url, setUrl] = useState('');
  const [email, setEmail] = useState('');
  const [result, setResult] = useState(null);

  const checkURL = () => {
    const warnings = [];
    let score = 0;

    // HTTPSチェック
    if (!url.toLowerCase().startsWith('https://')) {
      warnings.push('HTTPSを使用していません(セキュリティが低い)');
      score += 3;
    }

    // 疑わしいドメインパターン
    const suspiciousPatterns = [
      /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/, // IPアドレス
      /-/g, // 複数のハイフン
      /[а-я]/g, // キリル文字
      /\@/g, // @記号
    ];

    suspiciousPatterns.forEach(pattern => {
      if (pattern.test(url)) {
        warnings.push('疑わしい文字パターンが含まれています');
        score += 2;
      }
    });

    // 長すぎるURL
    if (url.length > 100) {
      warnings.push('URLが異常に長い');
      score += 2;
    }

    // よくあるフィッシングワード
    const phishingWords = ['secure', 'account', 'update', 'verify', 'login', 'bank'];
    phishingWords.forEach(word => {
      if (url.toLowerCase().includes(word)) {
        warnings.push(`「${word}」など注意が必要な単語が含まれています`);
        score += 1;
      }
    });

    setResult({
      type: 'url',
      score,
      warnings,
      level: score >= 5 ? 'danger' : score >= 2 ? 'warning' : 'safe'
    });
  };

  const checkEmail = () => {
    const warnings = [];
    let score = 0;

    // 緊急性を煽る表現
    const urgentWords = ['緊急', '今すぐ', '24時間以内', '本日中', '至急', '重要'];
    urgentWords.forEach(word => {
      if (email.includes(word)) {
        warnings.push(`緊急性を煽る表現「${word}」が含まれています`);
        score += 2;
      }
    });

    // 個人情報を要求
    const personalInfoWords = ['パスワード', '暗証番号', 'クレジットカード', '口座番号', '本人確認'];
    personalInfoWords.forEach(word => {
      if (email.includes(word)) {
        warnings.push(`個人情報「${word}」を要求している可能性があります`);
        score += 3;
      }
    });

    // リンククリックを促す
    if (email.includes('クリック') || email.includes('こちら') || email.includes('ログイン')) {
      warnings.push('リンクのクリックを促しています');
      score += 2;
    }

    // 不自然な日本語
    if (/[ぁ-ん]{20,}/.test(email) || /[ァ-ン]{20,}/.test(email)) {
      warnings.push('不自然な日本語が含まれている可能性があります');
      score += 1;
    }

    setResult({
      type: 'email',
      score,
      warnings,
      level: score >= 5 ? 'danger' : score >= 2 ? 'warning' : 'safe'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <div className="flex items-center gap-3 mb-6">
            <Shield className="w-10 h-10 text-indigo-600" />
            <h1 className="text-3xl font-bold text-gray-800">
              フィッシング詐欺チェッカー
            </h1>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            {/* URLチェック */}
            <div className="border-2 border-gray-200 rounded-xl p-6 hover:border-indigo-300 transition">
              <div className="flex items-center gap-2 mb-4">
                <Link className="w-6 h-6 text-indigo-600" />
                <h2 className="text-xl font-semibold">URLチェック</h2>
              </div>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                className="w-full p-3 border-2 border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-indigo-500"
              />
              <button
                onClick={checkURL}
                disabled={!url}
                className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-300 transition"
              >
                URLを確認
              </button>
            </div>

            {/* メール/メッセージチェック */}
            <div className="border-2 border-gray-200 rounded-xl p-6 hover:border-indigo-300 transition">
              <div className="flex items-center gap-2 mb-4">
                <Mail className="w-6 h-6 text-indigo-600" />
                <h2 className="text-xl font-semibold">メッセージチェック</h2>
              </div>
              <textarea
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="メールやメッセージの内容を入力..."
                className="w-full p-3 border-2 border-gray-300 rounded-lg mb-4 h-24 resize-none focus:outline-none focus:border-indigo-500"
              />
              <button
                onClick={checkEmail}
                disabled={!email}
                className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-300 transition"
              >
                メッセージを確認
              </button>
            </div>
          </div>

          {/* 結果表示 */}
          {result && (
            <div className={`rounded-xl p-6 ${
              result.level === 'danger' ? 'bg-red-50 border-2 border-red-300' :
              result.level === 'warning' ? 'bg-yellow-50 border-2 border-yellow-300' :
              'bg-green-50 border-2 border-green-300'
            }`}>
              <div className="flex items-center gap-3 mb-4">
                {result.level === 'danger' && <AlertTriangle className="w-8 h-8 text-red-600" />}
                {result.level === 'warning' && <AlertTriangle className="w-8 h-8 text-yellow-600" />}
                {result.level === 'safe' && <CheckCircle className="w-8 h-8 text-green-600" />}
                <h3 className={`text-2xl font-bold ${
                  result.level === 'danger' ? 'text-red-700' :
                  result.level === 'warning' ? 'text-yellow-700' :
                  'text-green-700'
                }`}>
                  {result.level === 'danger' ? '⚠️ 高リスク' :
                   result.level === 'warning' ? '⚠️ 注意が必要' :
                   '✓ 安全性が高い'}
                </h3>
              </div>

              {result.warnings.length > 0 ? (
                <div>
                  <p className="font-semibold mb-2">検出された警告:</p>
                  <ul className="space-y-2">
                    {result.warnings.map((warning, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-red-500 mt-1">•</span>
                        <span>{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <p>疑わしい要素は検出されませんでした。ただし、常に注意を怠らないでください。</p>
              )}
            </div>
          )}
        </div>

        {/* 対策ガイド */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            📚 フィッシング詐欺対策のポイント
          </h2>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="font-semibold mb-2">✓ URLを必ず確認</p>
              <p className="text-gray-700">公式サイトのURLを事前に確認し、HTTPSであることを確認しましょう</p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="font-semibold mb-2">✓ 緊急性に惑わされない</p>
              <p className="text-gray-700">「今すぐ」「24時間以内」など焦らせる表現には注意</p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="font-semibold mb-2">✓ 個人情報は入力しない</p>
              <p className="text-gray-700">メールからのリンクで個人情報を入力するのは避けましょう</p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="font-semibold mb-2">✓ 公式アプリを使用</p>
              <p className="text-gray-700">メールのリンクではなく、公式アプリから直接アクセス</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}