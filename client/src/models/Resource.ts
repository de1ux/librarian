export interface ResourceModel<T> {
    count: number
    next: string
    previous: string
    results: Array<T>
}
