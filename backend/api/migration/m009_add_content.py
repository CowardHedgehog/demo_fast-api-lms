from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

import api.models.content as content_model

async def add_content(db: AsyncSession):
  rows = [
    content_model.Content(
      id = 1,
      content = "<h2><b><u>教科書コンテンツ01</u></b></h2>\n\n  $\\\\\\\\$\n  ここに教科書コンテンツが表示されます。  \n\n  $\\\\\\\\$\n  ### [Page01](flow/1)",
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 2,
      content = "<h2><b><u>教科書コンテンツ02</u></b></h2>\n\n  $\\\\\\\\$\n  ここに教科書コンテンツが表示されます。  \n\n  $\\\\\\\\$\n  ### [Page02](flow/2)",
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 3,
      content = "演習問題概要がここに表示されます",
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 4,
      content = "演習問題終了時のコメントがここに表示されます",
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 5,
      content = 'ここにヒントが表示されるよ！',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 6,
      content = 'ここに解説が表示されるよ！',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 7,
      content = '1-1_1 SingleTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 8,
      content = '1-2_1 SingleTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 9,
      content = '1-3_1 SingleTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 10,
      content = '1-1_2 SingleTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 11,
      content = '1-2_2 SingleTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 12,
      content = '1-3_2 SingleTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 13,
      content = '2-1 MultipleTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 14,
      content = '解答欄1:blank1,解答欄2:blank2',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 15,
      content = 'DescriptiveTextQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 16,
      content = 'ChoiceQuestionです',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 17,
      content = 'チョコレート',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 18,
      content = 'アイスクリーム',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 19,
      content = 'ポテトチップス',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    ),
    content_model.Content(
      id = 20,
      content = 'グミ',
      created = datetime(2024,4,1,0,0,0),
      last_updated = datetime(2024,4,1,0,0,0),
    )
  ]
  db.add_all(rows)
  await db.flush()