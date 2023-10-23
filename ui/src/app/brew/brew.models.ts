
export class Brew {
    constructor(json_obj: any) {
        this.name = json_obj.name;
        this.id = json_obj.id;
        this.remote_id = json_obj.remote_id;
        this.description = json_obj.description;
        this.start_time = new Date(json_obj.start_time);
        this.measurement_ids = json_obj.measurement_ids;
        this.active = json_obj.active;
        this.stages = []
        for (const measurement_json of json_obj.stages) {
            this.stages.push(new Stage(measurement_json))
        };
    }
    name: string
    id: number
    remote_id: string
    description?: string
    active: boolean
    start_time: Date
    measurement_ids: string[]
    stages: Stage[]

    getCurrentStage(): Stage {
        return this.stages[this.stages.length-1];
    }
    isComplete(): boolean {
        return this.getCurrentStage().stage_name == 'COMPLETE';
    }
    isFermenting(): boolean {
        return this.getCurrentStage().stage_name == 'FERMENTING';
    }
}

export class Stage {
    constructor(json_obj: any) {
        this.stage_name = json_obj.stage_name;
        this.start_time = new Date(json_obj.start_time);
        this.estimated_end_time = new Date(json_obj.estimated_end_time);
    }
    stage_name: string; // COMPLETE or BOTTLE_CONDITIONING or FERMENTING
    start_time: Date;
    estimated_end_time: Date;
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
        this.type = json_obj.type;
    }
    source_name: string
    measurements: Measurement[]
    brew_id: number
    brew_remote_id: string
    nickname?: string
    type: string // ALCOHOL or TEMPERATURE or HEATER

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