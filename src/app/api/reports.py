from fastapi import APIRouter, Depends
from ..services.reporting import ReportingService
from ..deps import get_reporting_service
from ..domain.models import AttendanceRow, RevenueRow, OrderStatsOut

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/attendance", response_model=list[AttendanceRow])
def attendance(svc: ReportingService = Depends(get_reporting_service)):
    rows = svc.attendance()
    return [
        AttendanceRow(
            event_id=r["EventId"],
            title=r["Title"],
            starts_at=r["StartsAt"],
            capacity=r["Capacity"],
            sold_count=r["SoldCount"],
            remaining=r["Remaining"],
        )
        for r in rows
    ]

@router.get("/revenue", response_model=list[RevenueRow])
def revenue(svc: ReportingService = Depends(get_reporting_service)):
    rows = svc.revenue()
    return [
        RevenueRow(
            event_id=r["EventId"],
            title=r["Title"],
            revenue=float(r["Revenue"] or 0.0),
            payments_count=r["PaymentsCount"],
        )
        for r in rows
    ]

@router.get("/stats", response_model=OrderStatsOut)
def stats(svc: ReportingService = Depends(get_reporting_service)):
    r = svc.order_stats()
    return OrderStatsOut(
        min_order=r["MinOrder"],
        max_order=r["MaxOrder"],
        avg_order=r["AvgOrder"],
        paid_orders=r["PaidOrders"],
    )
