export const processDate = (date) =>{
  if (date == null)
    return '未提出'
  else{
    const datetime = new Date(date)
    const year = ('00' + datetime.getFullYear()).slice(-2)
    const month = ('00' + (datetime.getMonth()+1)).slice(-2)
    const day = ('00' + datetime.getDate()).slice(-2)
    const hour = ('00' + datetime.getHours()).slice(-2)
    const minute = ('00' + datetime.getMinutes()).slice(-2)
    return year + '/' + month + '/' + day + ' ' + hour + ':' + minute
  }
}

export const splitDate = (date) =>{
  const datetime = new Date(date)
  const sDate = [...Array(5)]
  sDate[0] = ('0000' + datetime.getFullYear()).slice(-4)
  sDate[1] = ('00' + (datetime.getMonth()+1)).slice(-2)
  sDate[2] = ('00' + datetime.getDate()).slice(-2)
  sDate[3] = ('00' + datetime.getHours()).slice(-2)
  sDate[4] = ('00' + datetime.getMinutes()).slice(-2)
  return sDate
}

export const combineDate = (...sDate) =>{
  return sDate[0].toString().padStart(4, '0') + '-' + sDate[1].toString().padStart(2, '0') + '-' + sDate[2].toString().padStart(2, '0') + 'T' + sDate[3].toString().padStart(2, '0') + ':' + sDate[4].toString().padStart(2, '0') + ':00'
}

export const omittedText = (text, n) => {
  return text.length > n ? text.slice(0, n) + '...' : text
}