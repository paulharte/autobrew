
export class Brew {
    constructor(json_obj: any) {
        this.name = json_obj.name;
        this.id = json_obj.id;
        this.remote_id = json_obj.remote_id;
        this.description = json_obj.description;
        this.start_time = new Date(json_obj.start_time);
        this.measurement_ids = json_obj.measurement_ids;
        this.active = json_obj.active;
        this.current_stage = json_obj.current_stage;
    }
    name: string
    id: number
    remote_id: string
    description?: string
    active: boolean
    start_time: Date
    measurement_ids: string[]
    current_stage: string
}

export class MeasurementSeries {
    constructor(json_obj: any) {
        this.source_name = json_obj.source_name;
        this.measurements = [];
        for (const measurement_json of json_obj.measurements) {
            this.measurements.push(new Measurement(measurement_json))
        };
        this.brew_id = json_obj.brew_id;
        this.brew_remote_id = json_obj.brew_remote_id;
        this.nickname = json_obj.nickname;
    }
    source_name: string
    measurements: Measurement[]
    brew_id: number
    brew_remote_id: string
    nickname?: string

    public getDisplayName(): string {
        return this.nickname ? this.nickname : this.source_name
    }
}

export class Measurement {
    constructor(json_obj: any) {
        this.source_name = json_obj.source_name;
        this.time = new Date(json_obj.time);
        this.measurement_amt = json_obj.measurement_amt;
    }
    source_name: string
    time: Date
    measurement_amt: number
}