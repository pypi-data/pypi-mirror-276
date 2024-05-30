import enum
import os
import ctypes
import win32com
import win32com.client
import pythoncom
import win32timezone
import win32clipboard
from win32com.client import constants
from win32com.client import Dispatch, constants


class WdCollapseDirection(enum.IntEnum):
    wdCollapseEnd = 0
    wdCollapseStart = 1


class WdSaveOptions(enum.IntEnum):
    wdDoNotSaveChanges = 0
    wdPromptToSaveChanges = -2
    wdSaveChanges = -1


class WdSaveFormat(enum.IntEnum):
    wdFormatDocument = 0  # Microsoft Office Word 97 - 2003 binary file format.
    wdFormatDOSText = 4  # Microsoft DOS text format.
    wdFormatDOSTextLineBreaks = 5  # Microsoft DOS text with line breaks preserved.
    wdFormatEncodedText = 7  # Encoded text format.
    wdFormatFilteredHTML = 10  # Filtered HTML format.
    wdFormatFlatXML = 19  # Open XML file format saved as a single XML file.
    wdFormatFlatXMLMacroEnabled = 20  # Open XML file format with macros enabled saved as a single XML file.
    wdFormatFlatXMLTemplate = 21  # Open XML template format saved as a XML single file.
    wdFormatFlatXMLTemplateMacroEnabled = 22  # Open XML template format with macros enabled saved as a single XML file.
    wdFormatOpenDocumentText = 23  # .odt OpenDocument Text format.
    wdFormatHTML = 8  # Standard HTML format.
    wdFormatRTF = 6  # Rich text format (RTF).
    wdFormatStrictOpenXMLDocument = 24  # Strict Open XML document format.
    wdFormatTemplate = 1  # Word template format.
    wdFormatText = 2  # Microsoft Windows text format.
    wdFormatTextLineBreaks = 3  # Windows text format with line breaks preserved.
    wdFormatUnicodeText = 7  # Unicode text format.
    wdFormatWebArchive = 9  # Web archive format.
    wdFormatXML = 11  # Extensible Markup Language (XML) format.
    wdFormatDocument97 = 0  # Microsoft Word 97 document format.
    wdFormatDocumentDefault = 16  # .docx Word default document file format. For Word, this is the DOCX format.
    wdFormatPDF = 17  # PDF format.
    wdFormatTemplate97 = 1  # Word 97 template format.
    wdFormatXMLDocument = 12  # XML document format.
    wdFormatXMLDocumentMacroEnabled = 13  # XML document format with macros enabled.
    wdFormatXMLTemplate = 14  # XML template format.
    wdFormatXMLTemplateMacroEnabled = 15  # XML template format with macros enabled.
    wdFormatXPS = 18  # XPS format.


class WdParagraphAlignment(enum.IntEnum):
    wdAlignParagraphCenter = 1  # 居中。
    wdAlignParagraphDistribute = 4  # 段落字符被分布排列，以填满整个段落宽度。
    wdAlignParagraphJustify = 3  # 完全两端对齐。
    wdAlignParagraphJustifyHi = 7  # 两端对齐，字符高度压缩。
    wdAlignParagraphJustifyLow = 8  # 两端对齐，字符轻微压缩。
    wdAlignParagraphJustifyMed = 5  # 两端对齐，字符中度压缩。
    wdAlignParagraphLeft = 0  # 左对齐。
    wdAlignParagraphRight = 2  # 右对齐。
    wdAlignParagraphThaiJustify = 9  # 按照泰语格式布局两端对齐。


class WdReplace(enum.IntEnum):
    wdReplaceAll = 2  # 替换所有匹配项。
    wdReplaceNone = 0  # 不替换任何匹配项。
    wdReplaceOne = 1  # 替换遇到的第一个匹配项


'''
https://learn.microsoft.com/zh-cn/office/vba/api/overview/word/object-model
https://learn.microsoft.com/zh-cn/office/vba/api/word.selection.pasteandformat
https://learn.microsoft.com/zh-cn/office/vba/api/word.wdpasteoptions
https://learn.microsoft.com/zh-cn/office/vba/api/word.wdrecoverytype
https://learn.microsoft.com/zh-cn/office/vba/api/word.find.execute

'''


# 字体对象
class Font:
    _sizes = {
        "初号": 42, "小初": 36, "一号": 26, "小一": 24, "二号": 22, "小二": 18,
        "三号": 16, "小三": 15, "四号": 14, "小四": 12, "五号": 10, "小五": 9,
        "六号": 7, "小六": 6, "七号": 5,
    }

    def __init__(self, object):
        self.object = object

    # 大小
    @property
    def size(self) -> int:
        return self.object.Size

    @size.setter
    def size(self, v: [int, str]):
        if isinstance(v, str):
            v = self._sizes[v]
        self.object.Size = v


# 样式对象
class Style:
    def __init__(self, document, object):
        self.document: Document = document
        self.object = object

    # 获取样式名称
    @property
    def name(self):
        return self.object.NameLocal

    def __repr__(self):
        module_name = self.__module__
        class_name = type(self).__name__
        return f"{module_name}.{class_name}(name={repr(self.name)},)"


# 段落格式对象
class ParagraphFormat:
    def __init__(self, paragraph: 'Paragraph', object):
        self.paragraph = paragraph
        self.object = object  # .HangingPunctuation = True # 标点可以溢出边界。

    # 对齐方式
    @property
    def alignment(self) -> WdParagraphAlignment:
        return self.object.Alignment

    @alignment.setter
    def alignment(self, a: WdParagraphAlignment):
        self.object.Alignment = a


# 查找替换对象
class Find:
    _include_attribute = [
        "__dict__", "__class__", "document", "object",
    ]
    _exclude_attribute = [
        "Text", "Forward", "Wrap",
    ]
    Text: str  # 需要查找的文本
    Forward: bool  # 向前查找
    Wrap: int  # 自动在文档末尾从头开始查找

    def __init__(self, document: 'Document', object):
        self.document = document
        self.object = object
        '''
        Find.Text = ""
        Find.Forward = True 
        Find.Wrap = 1
        '''
        '''
        while self.execute():
            if self.found:
                match_range = self.parent
        
        '''

    # 执行查找/替换
    def execute(self) -> bool:
        return self.object.Execute()

    # 返回上次execute是否找到
    @property
    def found(self) -> bool:
        return self.object.Found

    # 返回上次execute匹配项所在的范围
    @property
    def parent(self):
        return Range(self.document, self.object.Parent)

    # 替换文本
    def replace(self, f: str, t: str, Replace=WdReplace.wdReplaceAll, MatchCase=True, MatchWildcards=False,
                **kwargs):
        self.object.Execute(FindText=f, ReplaceWith=t, Replace=Replace, MatchCase=MatchCase,
                            MatchWildcards=MatchWildcards, **kwargs)

    # 检查文本是否存在
    def contain(self, s: str, MatchCase=True, MatchWildcards=False,
                MatchPhrase=False, IgnoreSpace=False, IgnorePunct=False, **kwargs) -> bool:
        return self.object.Execute(FindText=s, MatchCase=MatchCase, MatchWildcards=MatchWildcards,
                                   # MatchPhrase=MatchPhrase, IgnoreSpace=IgnoreSpace, IgnorePunct=IgnorePunct,
                                   **kwargs)

    def __getattribute__(self, item):
        # __getattr__ 属性不存在在 __dict__ 里时才调用；__getattribute__ 总会被先调用。
        if (item in Find._include_attribute or item in dir(self)) and item not in Find._exclude_attribute:
            return super(Find, self).__getattribute__(item)
        return self.object.__getattribute__(item)

    def __setattr__(self, key, value):
        if (key in Find._include_attribute or key in dir(self)) and key not in Find._exclude_attribute:
            return super(Find, self).__setattr__(key, value)
        return self.object.__setattr__(key, value)


# 段落对象
class Paragraph:
    def __init__(self, document, object):
        self.document: Document = document
        self.object = object

    # 获取段落的范围
    def range(self):
        return Range(self.document, self.object.Range, self, )

    # 获取下一个段落
    def next(self) -> 'Paragraph':
        i = self.object.Next()
        return Paragraph(self.document, i)

    # 样式对象
    @property
    def style(self) -> Style:
        i = self.object.Style
        return Style(self.document, i)

    @style.setter
    def style(self, s: Style):
        self.object.Style = s.object

    # 获取段落样式
    @property
    def format(self) -> ParagraphFormat:
        return ParagraphFormat(self, self.object.Format)


# 选择对象
class Selection:
    def __init__(self, application, document, object):
        self.application: WordApplication = application
        self.document: Document = document
        self.object = object

    # 把选区的原点定位到
    def collapse(self, Direction=WdCollapseDirection.wdCollapseEnd):
        self.object.Collapse(Direction)

    # 粘贴
    def paste(self):
        self.object.Paste()

    # 选中范围内的内容
    def select(self):
        self.object.Select()

    # 取消选中
    def unselect(self, Direction=WdCollapseDirection.wdCollapseEnd):
        if Direction == WdCollapseDirection.wdCollapseEnd:
            self.object.Start = self.object.End
        elif Direction == WdCollapseDirection.wdCollapseStart:
            self.object.End = self.object.Start

    # 获取选择的范围
    def range(self):
        return Range(self.document, self.object.Range, )

    # 选择的开始与结束位置
    @property
    def position(self) -> tuple[int]:
        return self.object.Start, self.object.End

    @position.setter
    def position(self, start_end=(0, 0,)):
        self.object.Start, self.object.End, *_ = start_end


# 范围对象
class Range:
    def __init__(self, document, object, paragraph=None):
        self.document = document
        self.object = object
        self._paragraph: Paragraph = paragraph

    # 获取范围内的文本
    @property
    def text(self) -> str:
        return self.object.Text

    @text.setter
    def text(self, s: str):
        self.object.Text = s

    # 剪切范围里的数据到剪贴板
    def cut(self):
        self.object.Cut()

    # 删除范围里的文本
    def delete(self):
        self.object.Delete()

    # 复制范围里的数据到剪贴板
    def copy(self):
        self.object.Copy()

    # 选中范围内的内容
    def select(self):
        self.object.Select()

    # 取消选中
    def unselect(self, Direction=WdCollapseDirection.wdCollapseEnd):
        if Direction == WdCollapseDirection.wdCollapseEnd:
            self.object.Start = self.object.End
        elif Direction == WdCollapseDirection.wdCollapseStart:
            self.object.End = self.object.Start

    # 获取范围内的段落
    def paragraphs(self) -> list[Paragraph]:
        l = []
        for i in self.object.Paragraphs:
            o = Paragraph(self.document, i)
            l.append(o)
        return l

    # 获取范围的来源段落
    def paragraph(self) -> [Paragraph, None]:
        if self._paragraph is not None:
            try:
                _ = self._paragraph.range().text
            except AttributeError:
                self._paragraph = None
        return self._paragraph

    # Find对象
    def find(self) -> Find:
        return Find(self.document, self.object.Find)

    # 字体对象
    @property
    def font(self):
        return Font(self.object.Font)

    # 样式对象
    @property
    def style(self) -> Style:
        i = self.object.Style
        return Style(self.document, i)

    @style.setter
    def style(self, s: Style):
        self.object.Style = s.object

    # 范围的开始与结束位置
    @property
    def position(self) -> tuple[int]:
        return self.object.Start, self.object.End

    @position.setter
    def position(self, start_end=(0, 0,)):
        self.object.Start, self.object.End, *_ = start_end


# 文档对象
class Document:
    def __init__(self, application, file_path: str, object, ):
        self.application: WordApplication = application
        self.file_path = file_path
        self.object = object

    # 关闭文档
    def close(self, SaveChanges=WdSaveOptions.wdDoNotSaveChanges):
        self.object.Close(SaveChanges=SaveChanges)

    # 保存文档
    def save(self):
        self.object.Save()

    # 文档另存为 SaveAs2
    def save_as(self, file_path, FileFormat: WdSaveFormat = None, Encoding: [str, None] = None,
                **kwargs):
        file_path = os.path.normpath(file_path)
        self.object.SaveAs2(file_path, FileFormat=FileFormat, Encoding=Encoding, **kwargs)

    # 激活文档
    def activate(self):
        self.object.Activate()

    # 添加一个段落
    def add_paragraph(self):
        pass

    # 获取某个段落
    def paragraph(self, index=0) -> Paragraph:
        try:
            i = list(self.object.Paragraphs)[index]
        except Exception:
            raise
        else:
            return Paragraph(self, i)

    # 获取全部段落
    def paragraphs(self) -> list[Paragraph]:
        l = []
        for i in self.object.Paragraphs:
            o = Paragraph(self, i)
            l.append(o)
        return l

    # 全文范围对象
    def content(self) -> Range:
        return Range(self, self.object.Content, )

    # 获取样式对象
    def styles(self, key: [int, str]) -> Style:
        names = [i.NameLocal for i in self.object.Styles]
        if isinstance(key, str):
            if key not in names:
                raise KeyError(f"不存在样式：{key}")
        elif isinstance(key, int):
            key = names[key]
        i = self.object.Styles(key)
        return Style(self, i)


class WordApplication:
    def __init__(self, Visible=True, DisplayAlerts=True, **kwargs):
        self.documents = []

        self.a = win32com.client.gencache.EnsureDispatch('Word.Application')
        self.a.Visible = Visible
        self.a.DisplayAlerts = DisplayAlerts
        for k, v in kwargs.items():
            self.a.__setattr__(k, v)

    # 打开文档
    def open(self, file_path: str, Encoding='utf-8', ReadOnly=False, **kwargs) -> Document:
        file_path = os.path.normpath(file_path)
        object = self.a.Documents.Open(file_path, Encoding=Encoding, ReadOnly=ReadOnly, **kwargs)
        document = Document(self, file_path, object)
        self.documents.append(document)
        return document

    # 关闭所有文档
    def close_all(self):
        pass

    # 退出软件
    def quit(self):
        self.a.Quit()

    # 选择对象，光标
    def selection(self, document=None):
        if document is None:
            document = self.a.ActiveDocument
        document.activate()
        return Selection(self, document, self.a.Selection)
