$(document).ready(function () {
  // 最初はSubmitボタンを非表示にする
  $('.submit-button').hide();

  // <h5>要素がクリックされたときの処理

  $('h5').click(function () {
    // Submitボタンを表示
    $('.submit-button').show();

    // 関連する<img>要素のIDを取得
    var imgID = $(this).data('img-id');

    // 関連するページURLを取得
    var pageURL = $(this).data('page-url');

    // すべての<img>要素を非表示にする
    $('img').hide();

    // クリックされた<h5>要素に関連する<img>要素を表示
    $('#' + imgID).show();

    // ハイライトを追加
    $('h5').removeClass('highlighted-text'); // すべての<h5>要素からハイライトを削除
    $(this).addClass('highlighted-text'); // クリックされた<h5>要素にハイライトを追加

    // Submitボタンのリンクを設定
    $('.submit-button').attr('data-page-url', pageURL);
  });

  // Submitボタンがクリックされたときの処理
  $('.submit-button').click(function () {
    // ページ遷移
    var pageURL = $(this).data('page-url');
    window.location.href = pageURL;
  });
});
