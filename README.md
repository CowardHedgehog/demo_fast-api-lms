# fast-api-lms

## fast-api-lms の概要・基本機能

# FastAPI-LMS-Sample の概要

FastAPI-LMS には現在、クイズを受けたり、教科書コンテンツを閲覧する機能や、教師アカウントでログインした時は、学習コースの管理を行う機能が実装されています。

## ログイン画面

アプリを起動した後、以下のリンクを踏むとログインページに移ります。

http://localhost:8080/Login
<img width="941" alt="スクリーンショット 2022-05-19 15 52 37" src="https://user-images.githubusercontent.com/47232971/169228980-ec3acf9d-6ca9-4d4e-b042-2b8845c15fd8.png">

stud@user.comは学生用アカウントで、教科書コンテンツの閲覧と、クイズページの閲覧・回答、学習コース選択が可能です。

一方で、教師アカウント(teach@user.com)でログインすると、教師用のページに遷移し、学習コースの追加・期限編集などの管理が行えます。
<img width="843" alt="スクリーンショット 2022-05-19 16 21 31" src="https://user-images.githubusercontent.com/47232971/169235398-a0ac0df0-00c2-455c-94d0-58ee030dd186.png">

## ログアウト

ログアウトは、画面右上にあるところ LOGOUT の文字をクリックするとできます。
<img width="1015" alt="スクリーンショット 2022-05-24 9 23 49" src="https://user-images.githubusercontent.com/47232971/169924603-0be427e1-f544-48ee-8713-404a218031c0.png">

## 学習コース選択・追加（教師専用）

<img width="968" alt="スクリーンショット 2022-05-19 16 12 15" src="https://user-images.githubusercontent.com/47232971/169232367-6c87a3da-f481-4d6c-b9df-f080b80dd694.png">

## 新しいコースの追加

このページに sample_week1 という名前のフォルダをアップロードすることでサンプルの学習コース（sample_course でない方）が出来上がります。

基本的なコンテンツが掲載されたプロトタイプはこの新しく追加した方の学習コースで確認できます。

<img width="947" alt="スクリーンショット 2022-05-19 16 13 51" src="https://user-images.githubusercontent.com/47232971/169232525-5449363a-fd98-47c9-a5af-c0a42195dd7b.png">

## コースの管理

現在、コース管理ページからは、履修者の追加、コースの期限の設定、学習コース名の変更が行えます
<img width="947" alt="スクリーンショット 2022-05-19 16 18 15" src="https://user-images.githubusercontent.com/47232971/169234184-d97a4fce-78f7-44ab-af13-1913143d4acf.png">
<img width="954" alt="スクリーンショット 2022-05-19 16 18 21" src="https://user-images.githubusercontent.com/47232971/169234751-d6ffd2a2-8908-447d-be5e-f931cd8398e0.png">

## 学習コース選択画面

学生用アカウントでログインすると、以下のような学習コース選択画面に遷移します。
<img width="936" alt="スクリーンショット 2022-05-19 15 56 27" src="https://user-images.githubusercontent.com/47232971/169229636-f6f69392-8ba0-42ff-a41b-8f1c1a236e6d.png">

ここで提示されている学習コースをクリックすると学習コースのページに遷移します。

## 画面（教科書コンテンツ）

学習コース（１週目）に遷移すると、教科書のページが表示されます。
<img width="970" alt="スクリーンショット 2022-05-19 15 58 25" src="https://user-images.githubusercontent.com/47232971/169230050-2c77d23d-b4c3-4918-b481-a9b788b95a45.png">

このページを下の方にスクロールしていくと、「問題はこちら」と書かれたリンクがあり、そこをクリックすることで演習問題のフローページに遷移することができます。
<img width="987" alt="スクリーンショット 2022-05-19 16 00 12" src="https://user-images.githubusercontent.com/47232971/169230300-16c784a4-5b00-469a-ab73-0846f6457154.png">

## 演習問題のフローページ

演習問題のフローページからは、StartNewFlowSession ボタン、もしくはすでに受けてあるテストログの Start ボタンから演習問題のページに遷移することができます。

<img width="1000" alt="スクリーンショット 2022-05-19 16 02 33" src="https://user-images.githubusercontent.com/47232971/169230685-b1f1e64d-14c0-4b99-abfb-f982b83a99ea.png">

GoToCourse ボタンからは、またコースページに戻ることができます。

## 演習問題のページ

演習問題のページでは実際にクイズを受けることができます。クイズに回答すると、正誤判定が表示され、終了ボタンを押すと、クイズを終了し、クイズの開始時刻と終了時刻が記録されます。
<img width="949" alt="スクリーンショット 2022-05-19 16 05 37" src="https://user-images.githubusercontent.com/47232971/169231226-7a08b656-4999-4592-8290-0461368e81df.png">


docker-compose logs -f

でログが見れます。
