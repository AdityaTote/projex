from __future__ import annotations

from typing import List, TypedDict

from pydantic import BaseModel, ConfigDict


class ZohoBaseModel(BaseModel):
	model_config = ConfigDict(extra="allow")


class FilterCondition(TypedDict):
	field_name: str
	criteria_condition: str
	value: list[object]


class TaskFilter(TypedDict):
	criteria: list["FilterCondition"]
	pattern: str


class MemberRelativeColumn(TypedDict):
	cfid: str
	offset: str
	unit: str
	prior: str


class MemberFilterCondition(TypedDict):
	cfid: str
	api_name: str
	field_name: str
	criteria_condition: str
	value: list[str]
	relative_columns: list["MemberRelativeColumn"]


class MemberFilter(TypedDict):
	criteria: list["MemberFilterCondition"]
	pattern: str


class ReportFilterCondition(TypedDict):
	field_name: str
	criteria_condition: str
	value: list[str]


class ReportFilter(TypedDict):
	criteria: list["ReportFilterCondition"]
	pattern: str


class CustomRange(TypedDict):
	start_date: str
	end_date: str


class TaskListRef(ZohoBaseModel):
	id: str


class ParentInfo(ZohoBaseModel):
	parent_task_id: str | None = None


class StatusRef(ZohoBaseModel):
	id: str


class Duration(ZohoBaseModel):
	value: List[int]
	type: str


class OwnerWorkEntry(ZohoBaseModel):
	zpuid: str
	work_values: str | None = None


class OwnerWork(ZohoBaseModel):
	add: List[OwnerWorkEntry] | None = None
	remove: List[OwnerWorkEntry] | None = None
	zpuid: str | None = None
	work_values: str | None = None


class OwnersAndWork(ZohoBaseModel):
	owners: List[OwnerWork] | None = None
	work_type: str | None = None
	unit: str | None = None
	copy_task_duration: str | None = None


class TagChange(ZohoBaseModel):
	id: str


class TagEntry(ZohoBaseModel):
	add: List[TagChange] | None = None
	remove: List[TagChange] | None = None
	id: str | None = None


class TeamEntry(ZohoBaseModel):
	add: List[TagChange] | None = None
	remove: List[TagChange] | None = None
	id: str | None = None


class RetainConfig(ZohoBaseModel):
	comments: str | None = None
	billing_type: str | None = None
	followers: str | None = None
	description: str | None = None
	subtasks: str | None = None
	tags: str | None = None
	attachments: List[int] | None = None
	teams: str | None = None


class DateBasedRecurrence(ZohoBaseModel):
	field_name: str | None = None
	repetative_type: str | None = None
	time_span: str | None = None
	ends_after_type: str | None = None
	ends_after_value: str | None = None
	skip_type: str | None = None
	duration_type: str | None = None
	no_of_duration: str | None = None


class SchedulerBasedRecurrence(ZohoBaseModel):
	repetative_type: str | None = None
	time_span: str | None = None
	ends_after_type: str | None = None
	ends_after_value: str | None = None
	skip_type: str | None = None
	time: str | None = None
	days_of_week: str | None = None
	months_of_year: str | None = None
	repeat_on_type: str | None = None
	repeat_on_value: str | None = None


class Recurrence(ZohoBaseModel):
	trigger_type: str | None = None
	retain_config: RetainConfig | None = None
	date_based: DateBasedRecurrence | None = None
	scheduler_based: SchedulerBasedRecurrence | None = None


class BudgetInfo(ZohoBaseModel):
	rate_per_hour: str | None = None
	budget: str | None = None
	threshold: str | None = None
	revenue_budget: str | None = None
	cost_rate_per_hour: str | None = None


class TaskCreate(ZohoBaseModel):
	model_config = ConfigDict(extra="allow")

	tasklist: TaskListRef | None = None
	parental_info: ParentInfo | None = None
	name: str
	description: str | None = None
	status: StatusRef | None = None
	priority: str | None = None
	start_date: str | None = None
	end_date: str | None = None
	duration: Duration | None = None
	completion_percentage: str | None = None
	billing_type: str | None = None
	attachments: List[int] | None = None
	owners_and_work: OwnersAndWork | None = None
	tags: List[TagEntry] | None = None
	teams: List[TeamEntry] | None = None
	recurrence: Recurrence | None = None
	budget_info: BudgetInfo | None = None


class TaskUpdate(ZohoBaseModel):
	model_config = ConfigDict(extra="allow")

	tasklist: TaskListRef | None = None
	parental_info: ParentInfo | None = None
	name: str | None = None
	description: str | None = None
	status: StatusRef | None = None
	priority: str | None = None
	start_date: str | None = None
	end_date: str | None = None
	duration: Duration | None = None
	completion_percentage: str | None = None
	billing_type: str | None = None
	attachments: List[int] | None = None
	owners_and_work: OwnersAndWork | None = None
	tags: List[TagEntry] | None = None
	teams: List[TeamEntry] | None = None
	recurrence: Recurrence | None = None
	budget_info: BudgetInfo | None = None


class PortalOwner(ZohoBaseModel):
	zpuid: str | None = None
	full_name: str | None = None
	name: str | None = None
	last_name: str | None = None
	id: int | None = None
	is_client_user: bool | None = None
	first_name: str | None = None
	email: str | None = None


class PortalBusinessDetails(ZohoBaseModel):
	start_time: str | None = None
	data_format: str | None = None
	weekends: List[str] | None = None
	time_format: str | None = None
	working_days: List[str] | None = None
	week_start_day: int | None = None
	end_time: str | None = None
	week_start_year: int | None = None


class PortalPlanDetails(ZohoBaseModel):
	projects_service_plan: str | None = None
	bugtracker_service_plan: str | None = None


class PortalDetails(ZohoBaseModel):
	owner: PortalOwner | None = None
	business_details: PortalBusinessDetails | None = None
	logo_url: str | None = None
	timezone: str | None = None
	name: str | None = None
	id: int | None = None
	plan_details: PortalPlanDetails | None = None
	org_name: str | None = None
	is_customdomain_enabled: bool | None = None


class GetPortalIdResponse(ZohoBaseModel):
	portal_details: PortalDetails | None = None


class MoneyAmount(ZohoBaseModel):
	amount: float | None = None
	formatted_amount: str | None = None
	currency_code: str | None = None
	currency_id: str | None = None


class ProjectBudgetInfo(ZohoBaseModel):
	hourly_budget: str | None = None
	billing_method: str | None = None
	forecasted_cost: MoneyAmount | None = None
	planned_hours: str | None = None
	bcy_forecasted_cost: MoneyAmount | None = None
	forecasted_hours: str | None = None
	remaining_hours: str | None = None
	actual_cost: MoneyAmount | None = None
	actual_hours: str | None = None
	bcy_planned_cost: MoneyAmount | None = None
	planned_cost: MoneyAmount | None = None
	budget_type: str | None = None
	bcy_actual_cost: MoneyAmount | None = None
	cost_budget: MoneyAmount | None = None


class CountInfo(ZohoBaseModel):
	closed_count: int | None = None
	open_count: int | None = None


class ProjectUser(ZohoBaseModel):
	zpuid: str | None = None
	name: str | None = None
	last_name: str | None = None
	first_name: str | None = None
	zuid: str | int | None = None


class ProjectTag(ZohoBaseModel):
	id: str | None = None
	color_hexcode: str | None = None


class ProjectLayout(ZohoBaseModel):
	name: str | None = None
	id: str | None = None
	is_default: str | bool | None = None
	type: str | None = None


class ProjectGroup(ZohoBaseModel):
	name: str | None = None
	id: str | None = None
	type: str | None = None


class ProjectStatus(ZohoBaseModel):
	is_closed_type: str | bool | None = None
	name: str | None = None
	id: str | None = None


class ProjectItem(ZohoBaseModel):
	end_date: str | None = None
	picklist_11sep: str | None = None
	is_public_project: str | bool | None = None
	description: str | None = None
	is_strict_project: str | bool | None = None
	multiline_11sep: str | None = None
	budget_info: ProjectBudgetInfo | None = None
	issues: CountInfo | None = None
	is_completed: str | bool | None = None
	id: str | None = None
	key: str | None = None
	tasks: CountInfo | None = None
	number_11sep: str | None = None
	start_date: str | None = None
	phone_11sep: str | None = None
	project_type: str | None = None
	created_time: str | None = None
	check_box_sample_11sep: str | None = None
	is_rollup_project: str | bool | None = None
	one: str | None = None
	created_by: ProjectUser | None = None
	percent_complete: str | int | None = None
	tags: List[ProjectTag] | None = None
	layout: ProjectLayout | None = None
	completed_time: str | None = None
	single_line_test_1446: str | None = None
	name: str | None = None
	updated_by: ProjectUser | None = None
	project_group: ProjectGroup | None = None
	milestones: CountInfo | None = None
	status: ProjectStatus | None = None


class ListProjectsResponse(ZohoBaseModel):
	projects: List[ProjectItem] | None = None


class TaskStatus(ZohoBaseModel):
	id: str | None = None
	name: str | None = None
	color: str | None = None
	color_hexcode: str | None = None
	is_closed_type: bool | None = None


class TaskOwner(ZohoBaseModel):
	zuid: int | None = None
	zpuid: str | None = None
	name: str | None = None
	email: str | None = None
	first_name: str | None = None
	last_name: str | None = None
	work_values: str | None = None


class TaskOwnersAndWork(ZohoBaseModel):
	work_type: str | None = None
	total_work: str | None = None
	unit: str | None = None
	copy_task_duration: bool | None = None
	owners: List[TaskOwner] | None = None
	refresh_business_hours: bool | None = None


class TaskDuration(ZohoBaseModel):
	value: str | None = None
	type: str | None = None


class TaskSequence(ZohoBaseModel):
	sequence: int | None = None


class TaskCreatedBy(ZohoBaseModel):
	zuid: int | None = None
	zpuid: str | None = None
	name: str | None = None
	email: str | None = None
	first_name: str | None = None
	last_name: str | None = None


class TaskBudgetInfo(ZohoBaseModel):
	exchange_rate: float | None = None


class TaskCurrency(ZohoBaseModel):
	currency_code: str | None = None
	formatted_amount: str | None = None
	amount: float | None = None


class TaskConnectModule(ZohoBaseModel):
	id: str | None = None
	value: str | None = None


class TaskItem(ZohoBaseModel):
	tasklist: TaskListRef | None = None
	project: TaskListRef | None = None
	milestone: TaskListRef | None = None
	id: str | None = None
	prefix: str | None = None
	name: str | None = None
	description: str | None = None
	status: TaskStatus | None = None
	color: str | None = None
	priority: str | None = None
	owners_and_work: TaskOwnersAndWork | None = None
	duration: TaskDuration | None = None
	completion_percentage: int | None = None
	sequence: TaskSequence | None = None
	depth: int | None = None
	created_time: str | None = None
	last_modified_time: str | None = None
	is_completed: bool | None = None
	created_via: str | None = None
	created_by: TaskCreatedBy | None = None
	billing_type: str | None = None
	budget_info: TaskBudgetInfo | None = None
	recurrence: Recurrence | None = None
	log_hours: ZohoBaseModel | None = None
	association_info: ZohoBaseModel | None = None
	single_line: str | None = None
	multi_line: str | None = None
	pick_list: str | None = None
	multi_pick_list: List[str] | None = None
	user_pick_list: TaskCreatedBy | None = None
	mupl_sel_user: List[TaskCreatedBy] | None = None
	date: str | None = None
	date_time: str | None = None
	check_box: bool | None = None
	currency: TaskCurrency | None = None
	percentage: float | None = None
	number: int | None = None
	decimal: float | None = None
	formula: str | None = None
	email: str | None = None
	phone: str | None = None
	url: str | None = None
	long_url: str | None = None
	lookup_field: str | None = None
	connect_module_2: TaskConnectModule | None = None


class PageInfo(ZohoBaseModel):
	page: int | None = None
	per_page: int | None = None
	page_count: int | None = None
	has_next_page: bool | None = None
	count: str | None = None


class ListTasksResponse(ZohoBaseModel):
	page_info: PageInfo | None = None
	tasks: List[TaskItem] | None = None


class TaskDetailResponse(TaskItem):
	pass


class TaskCreateResponse(TaskItem):
	pass


class TaskUpdateResponse(TaskItem):
	pass


class DeleteTaskResponse(ZohoBaseModel):
	pass


class MemberRole(ZohoBaseModel):
	name: str | None = None
	id: str | None = None
	type: str | None = None


class MemberProfile(ZohoBaseModel):
	name: str | None = None
	id: str | None = None
	type: str | None = None
	is_default: bool | None = None


class MemberReportingTo(ZohoBaseModel):
	full_name: str | None = None
	last_name: str | None = None
	id: str | None = None
	first_name: str | None = None
	zuid: str | None = None


class MemberBudget(ZohoBaseModel):
	rate_per_hour: str | None = None
	cost_per_hour: str | None = None
	type: str | None = None


class ProjectMember(ZohoBaseModel):
	added_time: str | None = None
	is_active: bool | None = None
	role: MemberRole | None = None
	time_of_request: str | None = None
	is_confirmed: bool | None = None
	profile: MemberProfile | None = None
	last_name: str | None = None
	reporting_to: MemberReportingTo | None = None
	display_name: str | None = None
	full_name: str | None = None
	user_type: str | None = None
	id: str | None = None
	invoice: str | None = None
	first_name: str | None = None
	email: str | None = None
	status: str | None = None
	budget: MemberBudget | None = None


class ListProjectMembersResponse(ZohoBaseModel):
	page_info: PageInfo | None = None
	users: List[ProjectMember] | None = None


class TimesheetReportResponse(ZohoBaseModel):
	pass


class OAuthTokenResponse(ZohoBaseModel):
	access_token: str | None = None
	expires_in_sec: int | None = None
	scope: str | None = None
	api_domain: str | None = None
	token_type: str | None = None
	expires_in: int | None = None
	refresh_token: str | None = None
