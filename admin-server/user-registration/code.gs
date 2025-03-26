const SHEET_ID = ''; // ←ここにIDを入力

function doGet() {
  return HtmlService.createHtmlOutputFromFile('form');
}

function getExistingAccounts() {
  const sheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
  const data = sheet.getRange(2, 2, sheet.getLastRow() - 1).getValues(); // B列: アカウント名
  return data.flat().filter(String);
}

function registerUser(entry) {
  const sheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
  sheet.appendRow([entry.kubun, entry.accountName, entry.fullName, entry.slackId]);
}
