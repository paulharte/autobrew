
interface Brew {
    name: string
    id: number
    remote_id: string
    active: boolean
    start_time: Date
    measurement_ids: string[]
}

interface MeasurementSeries {
    source_name: string
    measurements: Measurement[]
    brew_id: number
    brew_remote_id: string
    nickname: string
}

interface Measurement {
    source_name: string
    time: Date
    measurement_amt: number
}