"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from espy_contact.util.enums import ResourceEnum, GradeLevel, Term


class Resource(BaseModel):
    """Type of resource can be Poll, Form Builder, Questionnaire, RichText, Video, Audio, File, Hyperlink."""

    id: Optional[int] = None
    title: str
    type: ResourceEnum
    lesson_id: int


class Lesson_note(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    lesson_id: Optional[int] = None


class Quiz(BaseModel):
    id: Optional[int] = None
    title: str
    question: str
    options: List[str]
    answer: str
    lesson_id: Optional[int] = None


class Lesson(BaseModel):  # defintion of biology, branches of biology
    id: Optional[int] = None
    title: str  # Intro to Biology
    quiz: Optional[Quiz] = None
    note: Optional[Lesson_note] = None
    assets: Optional[
        List[str]
    ] = []  # these are assets shared between users not same as resources
    resources: Optional[List[ResourceEnum]] = []
    topic_id: Optional[int] = None


class LessonDto(Lesson):
    class_id: Optional[int] = None


class Topic(BaseModel):  # Introduction to Biology
    id: Optional[int] = None
    title: str
    timestamp: Optional[datetime] = None
    subject_id: Optional[str] = None
    lessons: Optional[List[Lesson]] = []


class TopicDto(Topic):
    age: Optional[datetime] = datetime


class SubjectDto(BaseModel):
    id: Optional[int] = None
    title: str  # Biology
    class_id: Optional[str] = None  # Grade
    grade: Optional[GradeLevel] = None
    term: Term
    topics: Optional[List[Topic]] = None
    lesson_count: Optional[int] = 0


class ClassroomDto(BaseModel):
    id: Optional[int] = None
    title: str
    subjects: Optional[List[SubjectDto]]
    # teachers: List[Teacher]  # ManyToMany relationship with Teacher


class Review(BaseModel):
    id: Optional[int] = None
    title: str
    review: str
    rating: float
    reviewer: str
    created_at: datetime
    subject: SubjectDto
